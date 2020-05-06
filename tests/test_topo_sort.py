# pylint: disable=missing-docstring,invalid-name,redefined-outer-name,unused-argument

import pytest

from paradag import DAG
from paradag import dag_run
from paradag import SingleSelector, FullSelector, RandomSelector, ShuffleSelector


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


def check_sorted_vertices(vertices_sorted, dag):
    assert set(vertices_sorted) == dag.vertices()
    assert vertices_sorted.index(3) < vertices_sorted.index('c')
    assert vertices_sorted.index('c') < vertices_sorted.index('5ef')
    assert vertices_sorted.index('c') < vertices_sorted.index(15)
    assert vertices_sorted.index('c') < vertices_sorted.index('sg')
    assert vertices_sorted.index(678) < vertices_sorted.index(679)
    assert vertices_sorted.index(3) < vertices_sorted.index('5ef')
    assert vertices_sorted.index(678) < vertices_sorted.index(679)


@pytest.mark.parametrize('i', range(64))
def test_topo_sort_by_single_selector(i, dag):
    vertices_sorted = dag_run(dag, selector=SingleSelector())
    check_sorted_vertices(vertices_sorted, dag)


@pytest.mark.parametrize('i', range(64))
def test_topo_sort_by_full_selector(i, dag):
    vertices_sorted = dag_run(dag, selector=FullSelector())
    check_sorted_vertices(vertices_sorted, dag)


@pytest.mark.parametrize('i', range(64))
def test_topo_sort_by_random_selector(i, dag):
    vertices_sorted = dag_run(dag, selector=RandomSelector())
    check_sorted_vertices(vertices_sorted, dag)


@pytest.mark.parametrize('i', range(64))
def test_topo_sort_by_shuffle_selector(i, dag):
    vertices_sorted = dag_run(dag, selector=ShuffleSelector())
    check_sorted_vertices(vertices_sorted, dag)
