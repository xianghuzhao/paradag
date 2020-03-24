# pylint: disable=missing-docstring,invalid-name,redefined-outer-name

import copy
import pytest

from paradag import DAG
from paradag import DAGVertexNotFoundError, DAGEdgeNotFoundError, DAGCycleError


@pytest.fixture(scope='module')
def dag():
    d = DAG()
    d.add_vertex(3, 'c', '5ef', 'sg', 15, 678, 679)
    d.add_edge(3, 'c')
    d.add_edge('c', '5ef', 15, 'sg')
    d.add_edge(678, 679)
    d.add_edge(3, '5ef')
    d.add_edge('5ef', 'sg')
    return d


def test_invalid_vertex(dag):
    with pytest.raises(DAGVertexNotFoundError):
        dag.add_edge(3, 'arfs')
    with pytest.raises(DAGVertexNotFoundError):
        dag.add_edge(234, 'c')
    with pytest.raises(DAGVertexNotFoundError):
        dag.add_edge(234, 'arfs')
    with pytest.raises(DAGVertexNotFoundError):
        dag.predecessors(234)
    with pytest.raises(DAGVertexNotFoundError):
        dag.successors('ghj')


def test_remove_edge(dag):
    dag_cp = copy.deepcopy(dag)
    with pytest.raises(DAGVertexNotFoundError):
        dag_cp.remove_edge(999, 'arfs')
    with pytest.raises(DAGEdgeNotFoundError):
        dag_cp.remove_edge('c', 3)
    with pytest.raises(DAGEdgeNotFoundError):
        dag_cp.remove_edge('sg', 678)

    dag_cp.remove_edge(3, '5ef')
    dag_cp.remove_edge('c', 15)
    dag_cp.remove_edge('c', 'sg')


def test_cycle(dag):
    with pytest.raises(DAGCycleError):
        dag.add_edge('sg', 3)
    with pytest.raises(DAGCycleError):
        dag.add_edge(15, 3)
    with pytest.raises(DAGCycleError):
        dag.add_edge(15, 15)
    with pytest.raises(DAGCycleError):
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
