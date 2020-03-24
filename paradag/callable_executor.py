'''An example executor where the vertice are callable'''


class CallableExecutor(object):
    '''An example executor where the vertice are callable'''

    def param(self, vertex):
        '''Use vertex as param'''
        return vertex

    def execute(self, param_vertex):
        '''Call the vertex'''
        return param_vertex()

    def report_start(self, vertice):
        '''Report the start status'''
        for vertex in vertice:
            print('Vertex {0} start'.format(vertex))

    def report_finish(self, vertice_results):
        '''Report the finish status'''
        for vertex, result in vertice_results:
            print('Vertex {0} finished with result: {1}'.format(
                vertex, result))
