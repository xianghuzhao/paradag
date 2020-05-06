'''A processor which will run the executors in sequence'''

from paradag.error import VertexExecutionError


class SequentialProcessor(object):
    '''A processor which will run the executions in sequence'''

    def process(self, vertices_with_param, execute_func):
        '''Process vertices in sequence'''
        results = []
        for vtx, param in vertices_with_param:
            try:
                result = execute_func(param)
            except Exception as e:
                raise VertexExecutionError(
                    'Vertex "{0}" execution error: {1}'.format(vtx, e))
            results.append((vtx, result))
        return results
