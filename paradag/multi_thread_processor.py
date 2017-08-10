import threading

try:
    from Queue import Queue
except ImportError:
    from queue import Queue


class MultiThreadProcessor(object):
    def __init__(self, timeout=None):
        self.__timeout = timeout

        self.__dag_threads = {}
        self.__dag_queue = Queue()

    def process(self, vertice):
        return vertice

    def __wait_vertice(self, vertice_to_run):
        for vertex in vertice:
            self.__dag_threads[vertex] = DagThread(self.__dag_queue, vertex)
            self.__dag_threads[vertex].start()

        try:
            item = self.__queue_unit.get(timeout=self.__timeout)
        except Queue.Empty:
            pass


class VertexCmd(object):
    @staticmethod
    def select_vertice(running, idle):
        return idle

    def __init__(self):
        pass

class DagThread(threading.Thread):
    def __init__(self, dag_queue, vertex):
        self.__dag_queue = dag_queue
        self.__vertex = vertex
