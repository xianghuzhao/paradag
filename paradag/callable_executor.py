'''An example executor where the vertices are callable'''


class CallableExecutor(object):
    '''An example executor where the vertices are callable'''

    def param(self, vertex):
        '''Use vertex as param'''
        return vertex

    def execute(self, param_vertex):
        '''Call the vertex'''
        return param_vertex()

    def report_start(self, vertices):
        '''Report the start status'''
        for vertex in vertices:
            print('Vertex {0} start'.format(vertex))

    def report_finish(self, vertices_results):
        '''Report the finish status'''
        for vertex, result in vertices_results:
            print('Vertex {0} finished with result: {1}'.format(
                vertex, result))
