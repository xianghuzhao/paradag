'''Exceptions for paradag'''


class DAGVertexNotFoundError(Exception):
    '''Exception when vertex not found'''


class DAGEdgeNotFoundError(Exception):
    '''Exception when edge not found'''


class DAGCycleError(Exception):
    '''Exception when cycle detected'''


class VertexExecutionError(Exception):
    '''Exception in vertex execution'''
