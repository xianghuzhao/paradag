import pytest

from paradag import dag_run
from paradag.callable_executor import CallableExecutor
from paradag.multi_thread_processor import MultiThreadProcessor

def check_callable(vertice_sorted, dag_tuple):
    dag = dag_tuple
    assert set(vertice_sorted) == dag[0].vertice()
    assert dag[1].result == 1
    assert dag[2].result == 4
    assert dag[3].result == 9
    assert dag[4].result == 16
    assert dag[5].result == 25
    assert dag[1].call_time <= dag[2].call_time
    assert dag[1].call_time <= dag[3].call_time
    assert dag[2].call_time <= dag[4].call_time
    assert dag[3].call_time <= dag[4].call_time

def test_dag_run_with_callable_executor(dag_callable):
    for i in range(100):
        vertice_sorted = dag_run(dag_callable[0], executor=CallableExecutor())
        check_callable(vertice_sorted, dag_callable)

def test_dag_run_with_multi_thread_processor(dag_callable):
    for i in range(100):
        vertice_sorted = dag_run(dag_callable[0], processor=MultiThreadProcessor(), executor=CallableExecutor())
        check_callable(vertice_sorted, dag_callable)
