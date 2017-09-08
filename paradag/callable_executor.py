from paradag import NullExecutor

class CallableExecutor(NullExecutor):
    def param(self, vertex):
        return vertex

    def execute(self, param_vertex):
        return param_vertex()

    def report_start(self, vertice):
        for vertex in vertice:
            print('Vertex {0} start'.format(vertex))

    def report_finish(self, vertice_results):
        for vertex, result in vertice_results:
            print('Vertex {0} finished with result: {1}'.format(vertex, result))
