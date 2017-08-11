import threading

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty


def dag_thread(dag_queue, vertex, executor, param):
    try:
        result = executor.execute(param)
        good = True
    except Exception as e:
        result = str(e)
        good = False
    finally:
        dag_queue.put((vertex, good, result))


class MultiThreadProcessor(object):
    def __init__(self, timeout=None):
        self.__timeout = timeout

        self.__dag_threads = {}
        self.__dag_queue = Queue()

    def __start_vertice(self, vertice, executor):
        for vertex in vertice:
            param_vertex = executor.param(vertex)
            args = [self.__dag_queue, vertex, executor, param_vertex]
            self.__dag_threads[vertex] = threading.Thread(target=dag_thread, args=args)
            self.__dag_threads[vertex].start()

    def __wait_vertice(self):
        try:
            item = self.__dag_queue.get(timeout=self.__timeout)
            self.__dag_threads[item[0]].join()
            return [item]
        except Empty:
            return []

    def process(self, vertice, executor):
        self.__start_vertice(vertice, executor)
        return self.__wait_vertice()
