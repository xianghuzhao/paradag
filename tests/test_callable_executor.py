# pylint: disable=missing-docstring,invalid-name,redefined-outer-name,unused-argument

import datetime
import pytest

from paradag import DAG
from paradag import dag_run
from paradag import VertexExecutionError
from paradag import ShuffleSelector
from paradag import CallableExecutor, SequentialProcessor, MultiThreadProcessor


class SimpleCallable(object):
    def __init__(self, val):
        self.__val = val
        self.__call_time = None
        self.__result = None

    def __call__(self):
        self.__call_time = datetime.datetime.now()
        self.__result = 1024 / self.__val

    def __str__(self):
        return 'SimpleCallable: 1024/{0}'.format(self.__val)

    @property
    def call_time(self):
        return self.__call_time

    @property
    def result(self):
        return self.__result


@pytest.fixture(scope='function')
def dag_callable():
    d = DAG()
    s1 = SimpleCallable(1)
    s2 = SimpleCallable(2)
    s3 = SimpleCallable(4)
    s4 = SimpleCallable(8)
    s5 = SimpleCallable(16)
    d.add_vertex(s1, s2, s3, s4, s5)
    d.add_edge(s1, s2, s3)
    d.add_edge(s2, s4)
    d.add_edge(s3, s4)
    return (d, s1, s2, s3, s4, s5)


def check_callable(vertice_sorted, dag_tuple):
    dag = dag_tuple
    assert set(vertice_sorted) == dag[0].vertice()
    assert dag[1].result == 1024
    assert dag[2].result == 512
    assert dag[3].result == 256
    assert dag[4].result == 128
    assert dag[5].result == 64
    assert dag[1].call_time <= dag[2].call_time
    assert dag[1].call_time <= dag[3].call_time
    assert dag[2].call_time <= dag[4].call_time
    assert dag[3].call_time <= dag[4].call_time


@pytest.mark.parametrize('i', range(64))
def test_dag_run_sequential_processor(i, dag_callable):
    vertice_sorted = dag_run(dag_callable[0],
                             selector=ShuffleSelector(),
                             processor=SequentialProcessor(),
                             executor=CallableExecutor())
    check_callable(vertice_sorted, dag_callable)


@pytest.mark.parametrize('i', range(64))
def test_dag_run_multi_thread_processor(i, dag_callable):
    vertice_sorted = dag_run(dag_callable[0],
                             selector=ShuffleSelector(),
                             processor=MultiThreadProcessor(),
                             executor=CallableExecutor())
    check_callable(vertice_sorted, dag_callable)


@pytest.fixture(scope='function')
def dag_callable_with_exception():
    d = DAG()
    s1 = SimpleCallable(1)
    s2 = SimpleCallable(2)
    s3 = SimpleCallable(0)
    s4 = SimpleCallable(8)
    s5 = SimpleCallable(16)
    d.add_vertex(s1, s2, s3, s4, s5)
    d.add_edge(s1, s2, s3)
    d.add_edge(s2, s4)
    d.add_edge(s3, s4)
    return (d, s1, s2, s3, s4, s5)


def check_callable_with_exception(dag_tuple):
    dag = dag_tuple
    assert dag[1].result == 1024
    assert dag[3].result is None
    assert dag[4].result is None


@pytest.mark.parametrize('i', range(64))
def test_dag_run_sequential_processor_with_exception(i, dag_callable_with_exception):
    with pytest.raises(VertexExecutionError):
        dag_run(dag_callable_with_exception[0],
                selector=ShuffleSelector(),
                processor=SequentialProcessor(),
                executor=CallableExecutor())
    check_callable_with_exception(dag_callable_with_exception)


@pytest.mark.parametrize('i', range(64))
def test_dag_run_multi_thread_processor_with_exception(i, dag_callable_with_exception):
    with pytest.raises(VertexExecutionError):
        dag_run(dag_callable_with_exception[0],
                selector=ShuffleSelector(),
                processor=MultiThreadProcessor(),
                executor=CallableExecutor())
    check_callable_with_exception(dag_callable_with_exception)
