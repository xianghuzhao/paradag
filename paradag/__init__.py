'''paradag'''

import random

from paradag.sequential_processor import SequentialProcessor
from paradag.multi_thread_processor import MultiThreadProcessor
from paradag.callable_executor import CallableExecutor
from paradag.error import *


class _dagData(object):
    '''The internal data of DAG'''

    def __init__(self):
        self.__graph = {}
        self.__graph_reverse = {}

    def vertices(self):
        '''Get the vertices list'''
        return set(self.__graph.keys())

    def add_vertex(self, vertex):
        '''Add a new vertex'''
        if vertex not in self.__graph:
            self.__graph[vertex] = set()
            self.__graph_reverse[vertex] = set()

    def add_edge(self, v_from, v_to):
        '''Add an edge from one vertex to another'''
        self.__graph[v_from].add(v_to)
        self.__graph_reverse[v_to].add(v_from)

    def remove_edge(self, v_from, v_to):
        '''Remove an edge from one vertex to another'''
        self.__graph[v_from].remove(v_to)
        self.__graph_reverse[v_to].remove(v_from)

    def successors(self, vertex):
        '''Get the successors of the specified vertex'''
        return self.__graph[vertex]

    def predecessors(self, vertex):
        '''Get the predecessors of the specified vertex'''
        return self.__graph_reverse[vertex]


class DAG(object):
    '''DAG '''

    def __init__(self):
        self.__data = _dagData()

    def __validate_vertex(self, *vertices):
        for vtx in vertices:
            if vtx not in self.__data.vertices():
                raise DAGVertexNotFoundError(
                    'Vertex "{0}" does not belong to DAG'.format(vtx))

    def __has_path_to(self, v_from, v_to):
        if v_from == v_to:
            return True
        for vtx in self.__data.successors(v_from):
            if self.__has_path_to(vtx, v_to):
                return True
        return False

    def vertices(self):
        '''Get the vertices list'''
        return self.__data.vertices()

    def add_vertex(self, *vertices):
        '''Add one or more vertices'''
        for vtx in vertices:
            self.__data.add_vertex(vtx)

    def add_edge(self, v_from, *v_tos):
        '''Add edge(s) from one vertex to others'''
        self.__validate_vertex(v_from, *v_tos)

        for v_to in v_tos:
            if self.__has_path_to(v_to, v_from):        # pylint: disable=arguments-out-of-order
                raise DAGCycleError(
                    'Cycle if add edge from "{0}" to "{1}"'.format(v_from, v_to))
            self.__data.add_edge(v_from, v_to)

    def remove_edge(self, v_from, v_to):
        '''Remove an edge from one vertex to another'''
        self.__validate_vertex(v_from, v_to)
        if v_to not in self.__data.successors(v_from):
            raise DAGEdgeNotFoundError(
                'Edge not found from "{0}" to "{1}"'.format(v_from, v_to))

        self.__data.remove_edge(v_from, v_to)

    def vertex_size(self):
        '''Get the number of vertices'''
        return len(self.__data.vertices())

    def edge_size(self):
        '''Get the number of edges'''
        size = 0
        for vtx in self.__data.vertices():
            size += self.outdegree(vtx)
        return size

    def successors(self, vertex):
        '''Get the successors of the specified vertex'''
        self.__validate_vertex(vertex)
        return self.__data.successors(vertex)

    def predecessors(self, vertex):
        '''Get the predecessors of the specified vertex'''
        self.__validate_vertex(vertex)
        return self.__data.predecessors(vertex)

    def indegree(self, vertex):
        '''Get the indegree of the specified vertex'''
        return len(self.predecessors(vertex))

    def outdegree(self, vertex):
        '''Get the outdegree of the specified vertex'''
        return len(self.successors(vertex))

    def __endpoints(self, degree_callback):
        endpoints = set()
        for vtx in self.__data.vertices():
            if degree_callback(vtx) == 0:
                endpoints.add(vtx)
        return endpoints

    def all_starts(self):
        '''Get all the starting vertices'''
        return self.__endpoints(self.indegree)

    def all_terminals(self):
        '''Get all the terminating vertices'''
        return self.__endpoints(self.outdegree)


class SingleSelector(object):
    '''A selector just selects the next idle vertex'''

    def select(self, _, idle):
        '''Select the next idle vertex'''
        return [next(iter(idle))]


class FullSelector(object):
    '''A selector selects all the idle vertices'''

    def select(self, _, idle):
        '''Select all the idle vertices'''
        return list(idle)


class RandomSelector(object):
    '''A selector randomly selects one idle vertex'''

    def select(self, _, idle):
        '''Randomly selects one idle vertex'''
        return [random.choice(list(idle))]


class ShuffleSelector(object):
    '''A selector selects all the idle vertices with shuffled order'''

    def select(self, _, idle):
        '''Selects all the idle vertices with shuffled order'''
        idle_list = list(idle)
        random.shuffle(idle_list)
        return idle_list


class NullProcessor(object):
    '''A processor which ignores all the execution'''

    def process(self, vertices_with_param, _):
        '''Return all vertices with result None'''
        return [(vtx, None) for vtx, _ in vertices_with_param]


class NullExecutor(object):
    '''An executor which runs no real things'''


def _call_method(instance, method, *args, **kwargs):
    try:
        func = getattr(instance, method)
    except AttributeError:
        return None

    if not callable(func):
        return None

    return func(*args, **kwargs)


def _process_vertices(vertices_to_run, vertices_running, processor, executor):
    def execute_func(param):
        return _call_method(executor, 'execute', param)

    vertices_with_param = [(vtx, _call_method(executor, 'param', vtx))
                           for vtx in vertices_to_run]
    try:
        return processor.process(vertices_with_param, execute_func)
    except VertexExecutionError:
        _call_method(executor, 'abort', vertices_running)
        _call_method(processor, 'abort')
        raise


def dag_run(dag, selector=FullSelector(), processor=NullProcessor(), executor=NullExecutor()):
    '''Run tasks according to DAG'''

    indegree_dict = {}
    for vtx in dag.vertices():
        indegree_dict[vtx] = dag.indegree(vtx)

    vertices_final = []
    vertices_running = set()
    vertices_zero_indegree = dag.all_starts()

    while vertices_zero_indegree:
        vertices_idle = vertices_zero_indegree-vertices_running
        vertices_to_run = selector.select(vertices_running, vertices_idle)
        _call_method(executor, 'report_start', vertices_to_run)

        vertices_running |= set(vertices_to_run)
        _call_method(executor, 'report_running', vertices_running)

        processed_results = _process_vertices(
            vertices_to_run, vertices_running, processor, executor)
        _call_method(executor, 'report_finish', processed_results)

        vertices_processed = [result[0] for result in processed_results]
        vertices_running -= set(vertices_processed)

        vertices_final += vertices_processed
        vertices_zero_indegree -= set(vertices_processed)

        for vtx, result in processed_results:
            for v_to in dag.successors(vtx):
                _call_method(executor, 'deliver', v_to, result)

                indegree_dict[v_to] -= 1
                if indegree_dict[v_to] == 0:
                    vertices_zero_indegree.add(v_to)

    return vertices_final
