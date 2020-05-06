'''A processor which will run the executors in parallel'''

import threading

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty

from paradag.error import VertexExecutionError


def _dag_execution(dag_queue, vertex, execute_func, param):
    '''Thread function for parallel execution'''
    try:
        dag_queue.put((vertex, execute_func(param)))
    except Exception as e:      # pylint: disable=broad-except
        dag_queue.put((vertex, e))


class MultiThreadProcessor(object):
    '''A processor which will run the executions in parallel'''

    def __init__(self, timeout=None):
        self.__timeout = timeout

        self.__dag_threads = {}
        self.__dag_queue = Queue()

    def __start_threads(self, vertices_with_param, execute_func):
        for vtx, param in vertices_with_param:
            if vtx not in self.__dag_threads:
                args = [self.__dag_queue, vtx, execute_func, param]
                self.__dag_threads[vtx] = threading.Thread(
                    target=_dag_execution, args=args)
                self.__dag_threads[vtx].start()

    def __wait_threads(self):
        if not self.__dag_threads:
            return []

        try:
            item = self.__dag_queue.get(timeout=self.__timeout)
            self.__dag_threads[item[0]].join()
            del self.__dag_threads[item[0]]

            if isinstance(item[1], Exception):
                raise VertexExecutionError(
                    'Vertex "{0}" execution error: {1}'.format(item[0], item[1]))

            return [item]
        except Empty:
            return []

    def process(self, vertices_with_param, execute_func):
        '''Process vertices in parallel'''
        self.__start_threads(vertices_with_param, execute_func)
        return self.__wait_threads()

    def abort(self):
        '''Quit all the threads'''
        while self.__dag_threads:
            item = self.__dag_queue.get()
            self.__dag_threads[item[0]].join()
            del self.__dag_threads[item[0]]
