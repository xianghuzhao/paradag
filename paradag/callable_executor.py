from paradag import NullExecutor

class CallableExecutor(NullExecutor):
    def param(self, vertex):
        return vertex

    def execute(self, param_vertex):
        return param_vertex()

    def report(self, vertex, result):
        if isinstance(result, Exception):
            print('Vertex {0} finished with exception: {1}'.format(vertex, result))
        else:
            print('Vertex {0} finished with result: {1}'.format(vertex, result))
