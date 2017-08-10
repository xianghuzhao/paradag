import random
import copy


class DagVertexNotFoundError(Exception):
    pass

class DagEdgeNotFoundError(Exception):
    pass

class DagCycleError(Exception):
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
    def __init__(self, data=DagData()):
        self.__data = data

    def __validate_vertex(self, *vertice):
        for vertex in vertice:
            if vertex not in self.__data.vertice():
                raise DagVertexNotFoundError('Vertex "%s" does not belong to DAG' % vertex)

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
                raise DagCycleError('Cycle if add edge from "%s" to "%s"' % (v_from, v_to))
            self.__data.add_edge(v_from, v_to)

    def remove_edge(self, v_from, v_to):
        self.__validate_vertex(v_from, v_to)
        if v_to not in self.__data.successors(v_from):
            raise DagEdgeNotFoundError('Edge not found from "%s" to "%s"' % (v_from, v_to))

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


def topo_sort(dag):
    dag_temp = copy.deepcopy(dag)

    sorted_vertice = []
    vertice_zero_indegree = dag_temp.all_starts()

    while vertice_zero_indegree:
        vertex = random.choice(list(vertice_zero_indegree))
        sorted_vertice.append(vertex)
        vertice_zero_indegree.remove(vertex)

        for v_to in dag_temp.successors(vertex).copy():
            dag_temp.remove_edge(vertex, v_to)
            if dag_temp.indegree(v_to) == 0:
                vertice_zero_indegree.add(v_to)

    return sorted_vertice
