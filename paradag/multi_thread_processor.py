import threading

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty

from paradag import VertexExecutionError


def dag_thread(dag_queue, vertex, executor, param):
    try:
        dag_queue.put((vertex, executor.execute(param)))
    except Exception as e:
        dag_queue.put((vertex, e))


class MultiThreadProcessor(object):
    def __init__(self, timeout=None):
        self.__timeout = timeout

        self.__dag_threads = {}
        self.__dag_queue = Queue()

    def __start_threads(self, vertice, executor):
        for vertex in vertice:
            if vertex not in self.__dag_threads:
                param_vertex = executor.param(vertex)
                args = [self.__dag_queue, vertex, executor, param_vertex]
                self.__dag_threads[vertex] = threading.Thread(target=dag_thread, args=args)
                self.__dag_threads[vertex].start()

    def __wait_threads(self, executor):
        try:
            item = self.__dag_queue.get(timeout=self.__timeout)
            self.__dag_threads[item[0]].join()
            del self.__dag_threads[item[0]]

            if isinstance(item[1], Exception):
                self.__clear_threads(executor)
                raise VertexExecutionError('Vertex "{0}" execution error: {1}'.format(item[0], item[1]))

            return [item]
        except Empty:
            return []

    def __clear_threads(self, executor):
        executor.abort(set(self.__dag_threads.keys()))

        while self.__dag_threads:
            item = self.__dag_queue.get()
            self.__dag_threads[item[0]].join()
            del self.__dag_threads[item[0]]

    def process(self, vertice, executor):
        self.__start_threads(vertice, executor)
        return self.__wait_threads(executor)
