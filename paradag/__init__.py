import random


class DagVertexNotFoundError(Exception):
    pass

class DagEdgeNotFoundError(Exception):
    pass

class DagCycleError(Exception):
    pass

class VertexExecutionError(Exception):
    pass


class DagData(object):
    def __init__(self):
        self.__graph = {}
        self.__graph_reverse = {}

    def vertice(self):
        return set(self.__graph.keys())

    def add_vertex(self, vertex):
        if vertex not in self.__graph:
            self.__graph[vertex] = set()
            self.__graph_reverse[vertex] = set()

    def add_edge(self, v_from, v_to):
        self.__graph[v_from].add(v_to)
        self.__graph_reverse[v_to].add(v_from)

    def remove_edge(self, v_from, v_to):
        self.__graph[v_from].remove(v_to)
        self.__graph_reverse[v_to].remove(v_from)

    def successors(self, vertex):
        return self.__graph[vertex]

    def predecessors(self, vertex):
        return self.__graph_reverse[vertex]


class Dag(object):
    def __init__(self):
        self.__data = DagData()

    def __validate_vertex(self, *vertice):
        for vertex in vertice:
            if vertex not in self.__data.vertice():
                raise DagVertexNotFoundError('Vertex "{0}" does not belong to DAG'.format(vertex))

    def __has_path_to(self, v_from, v_to):
        if v_from == v_to:
            return True
        for v in self.__data.successors(v_from):
            if self.__has_path_to(v, v_to):
                return True
        return False


    def vertice(self):
        return self.__data.vertice()

    def add_vertex(self, *vertice):
        for vertex in vertice:
            self.__data.add_vertex(vertex)

    def add_edge(self, v_from, *v_tos):
        self.__validate_vertex(v_from, *v_tos)

        for v_to in v_tos:
            if self.__has_path_to(v_to, v_from):
                raise DagCycleError('Cycle if add edge from "{0}" to "{1}"'.format(v_from, v_to))
            self.__data.add_edge(v_from, v_to)

    def remove_edge(self, v_from, v_to):
        self.__validate_vertex(v_from, v_to)
        if v_to not in self.__data.successors(v_from):
            raise DagEdgeNotFoundError('Edge not found from "{0}" to "{1}"'.format(v_from, v_to))

        self.__data.remove_edge(v_from, v_to)


    def vertex_size(self):
        return len(self.__data.vertice())

    def edge_size(self):
        size = 0
        for vertex in self.__data.vertice():
            size += self.outdegree(vertex)
        return size


    def successors(self, vertex):
        self.__validate_vertex(vertex)
        return self.__data.successors(vertex)

    def predecessors(self, vertex):
        self.__validate_vertex(vertex)
        return self.__data.predecessors(vertex)

    def indegree(self, vertex):
        return len(self.predecessors(vertex))

    def outdegree(self, vertex):
        return len(self.successors(vertex))


    def __endpoints(self, degree_callback):
        endpoints = set()
        for vertex in self.__data.vertice():
            if degree_callback(vertex) == 0:
                endpoints.add(vertex)
        return endpoints

    def all_starts(self):
        return self.__endpoints(self.indegree)

    def all_terminals(self):
        return self.__endpoints(self.outdegree)



class SingleSelector(object):
    def select(self, running, idle):
        return [next(iter(idle))]

class FullSelector(object):
    def select(self, running, idle):
        return list(idle)

class RandomSelector(object):
    def select(self, running, idle):
        return [random.choice(list(idle))]

class ShuffleSelector(object):
    def select(self, running, idle):
        idle_list = list(idle)
        random.shuffle(idle_list)
        return idle_list


class NullProcessor(object):
    def process(self, vertice, executor):
        return [(vertex, None) for vertex in vertice]


class NullExecutor(object):
    def param(self, vertex):
        return None

    def execute(self, param_vertex):
        return None

    def report(self, vertex, result):
        pass

    def deliver(self, vertex, result):
        pass

    def abort(self, vertice):
        pass


def dag_run(dag, selector=None, processor=None, executor=None):
    if selector is None:
        selector = FullSelector()
    if processor is None:
        processor = NullProcessor()
    if executor is None:
        executor = NullExecutor()

    indegree_dict = {}
    for vertex in dag.vertice():
        indegree_dict[vertex] = dag.indegree(vertex)

    vertice_final = []
    vertice_processing = set()
    vertice_zero_indegree = dag.all_starts()

    while vertice_zero_indegree:
        vertice_to_run = selector.select(vertice_processing, vertice_zero_indegree-vertice_processing)

        vertice_processed_results = processor.process(vertice_to_run, executor)
        vertice_processed = [result[0] for result in vertice_processed_results]

        vertice_processing |= set(vertice_to_run)
        vertice_processing -= set(vertice_processed)

        vertice_final += vertice_processed
        vertice_zero_indegree -= set(vertice_processed)

        for vertex, result in vertice_processed_results:
            executor.report(vertex, result)

            for v_to in dag.successors(vertex):
                executor.deliver(v_to, result)

                indegree_dict[v_to] -= 1
                if indegree_dict[v_to] == 0:
                    vertice_zero_indegree.add(v_to)

    return vertice_final
