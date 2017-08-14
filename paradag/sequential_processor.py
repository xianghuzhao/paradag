from paradag import VertexExecutionError

class SequentialProcessor(object):
    def process(self, vertice, executor):
        results = []
        for vertex in vertice:
            try:
                result = executor.execute(executor.param(vertex))
            except Exception as e:
                raise VertexExecutionError('Vertex "{0}" execution error: {1}'.format(vertex, e))
            results.append((vertex, result))
        return results
