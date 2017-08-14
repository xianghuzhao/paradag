import pytest

from paradag import Dag
from paradag import dag_run
from paradag import SingleSelector, FullSelector, RandomSelector, ShuffleSelector

@pytest.fixture(scope='module')
def dag():
    d = Dag()
    d.add_vertex(3, 'c', '5ef', 'sg', 15, 678, 679)
    d.add_edge(3, 'c')
    d.add_edge('c', '5ef', 15, 'sg')
    d.add_edge(678, 679)
    d.add_edge(3, '5ef')
    d.add_edge('5ef', 'sg')
    return d

def check_sorted_vertice(vertice_sorted, dag):
    assert set(vertice_sorted) == dag.vertice()
    assert vertice_sorted.index(3)   < vertice_sorted.index('c')
    assert vertice_sorted.index('c') < vertice_sorted.index('5ef')
    assert vertice_sorted.index('c') < vertice_sorted.index(15)
    assert vertice_sorted.index('c') < vertice_sorted.index('sg')
    assert vertice_sorted.index(678) < vertice_sorted.index(679)
    assert vertice_sorted.index(3)   < vertice_sorted.index('5ef')
    assert vertice_sorted.index(678) < vertice_sorted.index(679)

@pytest.mark.parametrize('i', range(64))
def test_topo_sort_by_single_selector(i, dag):
    vertice_sorted = dag_run(dag, selector=SingleSelector())
    check_sorted_vertice(vertice_sorted, dag)

@pytest.mark.parametrize('i', range(64))
def test_topo_sort_by_full_selector(i, dag):
    vertice_sorted = dag_run(dag, selector=FullSelector())
    check_sorted_vertice(vertice_sorted, dag)

@pytest.mark.parametrize('i', range(64))
def test_topo_sort_by_random_selector(i, dag):
    vertice_sorted = dag_run(dag, selector=RandomSelector())
    check_sorted_vertice(vertice_sorted, dag)

@pytest.mark.parametrize('i', range(64))
def test_topo_sort_by_shuffle_selector(i, dag):
    vertice_sorted = dag_run(dag, selector=ShuffleSelector())
    check_sorted_vertice(vertice_sorted, dag)
