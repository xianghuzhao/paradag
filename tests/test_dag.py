import pytest

from paradag import Dag
from paradag import topo_sort
from paradag import DagVertexNotFoundError, DagEdgeNotFoundError, DagCycleError

@pytest.fixture(scope='module')
def dag():
    dag = Dag()
    dag.add_vertex(3, 'c', '5ef', 'sg', 15, 678, 679)
    dag.add_edge(3, 'c')
    dag.add_edge('c', '5ef', 15, 'sg')
    dag.add_edge(678, 679)
    dag.add_edge(3, '5ef')
    dag.add_edge('5ef', 'sg')
    return dag

def test_invalid_vertex(dag):
    with pytest.raises(DagVertexNotFoundError):
        dag.add_edge(3, 'arfs')
    with pytest.raises(DagVertexNotFoundError):
        dag.add_edge(234, 'c')
    with pytest.raises(DagVertexNotFoundError):
        dag.add_edge(234, 'arfs')
    with pytest.raises(DagVertexNotFoundError):
        dag.predecessors(234)
    with pytest.raises(DagVertexNotFoundError):
        dag.successors('ghj')

def test_cycle(dag):
    with pytest.raises(DagCycleError):
        dag.add_edge('sg', 3)
    with pytest.raises(DagCycleError):
        dag.add_edge(15, 3)
    with pytest.raises(DagCycleError):
        dag.add_edge(15, 15)
    with pytest.raises(DagCycleError):
        dag.add_edge(679, 678)

def test_vertex_size(dag):
    assert dag.vertex_size() == 7

def test_edge_size(dag):
    assert dag.edge_size() == 7

def test_successors(dag):
    assert dag.successors('c') == set(['sg', '5ef', 15])

def test_predecessors(dag):
    assert dag.predecessors('5ef') == set(['c', 3])

def test_starts(dag):
    assert dag.all_starts() == set([678, 3])

def test_terminals(dag):
    assert dag.all_terminals() == set(['sg', 679, 15])

def test_topo_sort(dag):
    for i in range(1000):
        sorted_vertice = topo_sort(dag)
        assert set(sorted_vertice) == dag.vertice()
        assert sorted_vertice.index(3) < sorted_vertice.index('c')
        assert sorted_vertice.index('c') < sorted_vertice.index('5ef')
        assert sorted_vertice.index('c') < sorted_vertice.index(15)
        assert sorted_vertice.index('c') < sorted_vertice.index('sg')
        assert sorted_vertice.index(678) < sorted_vertice.index(679)
        assert sorted_vertice.index(3) < sorted_vertice.index('5ef')
        assert sorted_vertice.index(678) < sorted_vertice.index(679)