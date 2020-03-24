# paradag

[![PyPI](https://badge.fury.io/py/paradag.svg)](https://badge.fury.io/py/paradag)
[![Travis CI Status](https://travis-ci.org/xianghuzhao/paradag.svg?branch=master)](https://travis-ci.org/xianghuzhao/paradag)
[![Code Climate](https://codeclimate.com/github/xianghuzhao/paradag/badges/gpa.svg)](https://codeclimate.com/github/xianghuzhao/paradag)

`paradag` a robust DAG package for easy parallel execution.
`paradag` is implemented in pure python and totally independent of any
third party packages.

[Directed acyclic graph (DAG)](https://en.wikipedia.org/wiki/Directed_acyclic_graph)
is commonly used as a dependency graph. It could be used to describe the
dependencies of tasks.
The order of task executions must comply with the dependencies,
where tasks with direct or indirect path must run in sequence,
and tasks without any connection could run in parallel.


## Installation

```shell
$ pip install paradag
```


## Create a DAG

Before running tasks, first create a DAG,
with each vertex representing a task.
The vertex of DAG instance could be any
[hashable object](https://docs.python.org/3/glossary.html#term-hashable),
like integer, string, tuple of hashable objects, instance of
user-defined class, etc.

```python
from paradag import DAG

class Vtx(object):
    def __init__(self, v):
        self.__value = v

vtx = Vtx(999)

dag = DAG()
dag.add_vertex(123, 'abcde', 'xyz', ('a', 'b', 3), vtx)

dag.add_edge(123, 'abcde')                  # 123 -> 'abcde'
dag.add_edge('abcde', ('a', 'b', 3), vtx)   # 'abcde' -> ('a', 'b', 3), 'abcde' -> vtx
```

`add_edge` accepts one vertex as the predecessor and
one or more vertice as the successors.
Please pay attention not to make a cycle with `add_edge`,
which will raise a `DAGCycleError`.

The common DAG properties are accessible:

```python
print(dag.vertex_size())
print(dag.edge_size())

print(dag.successors('abcde'))
print(dag.predecessors(vtx))

print(dag.all_starts())
print(dag.all_terminals())
```


## Run tasks in sequence

Write your executor and optionally a selector.
The executor handles the real execution for each vertex.

```python
from paradag import dag_run
from paradag.sequential_processor import SequentialProcessor

class CustomExecutor:
    def param(self, vertex):
        return vertex

    def execute(self, param):
        print('Executing:', param)

print(dag_run(dag, processor=SequentialProcessor(), executor=CustomExecutor()))
```


## Run tasks in parallel

Run tasks in parallel is quite similar, while only change the processor
to `MultiThreadProcessor`.

```python
from paradag.multi_thread_processor import MultiThreadProcessor

dag_run(dag, processor=MultiThreadProcessor(), executor=CustomExecutor())
```

The default selector `FullSelector` will try to find as many tasks
as possible which could run in parallel.
This could be adjusted with custom selector.
The following selector will only allow at most 4 tasks running in parallel.

```python
class CustomSelector(object):
    def select(self, running, idle):
        task_number = max(0, 4-len(running))
        return list(idle)[:task_number]

dag_run(dag, processor=MultiThreadProcessor(), selector=CustomSelector(), executor=CustomExecutor())
```

Once you are using `MultiThreadProcessor`, great attentions must be
paid that `execute` of executor could run in parallel. Try not to modify
any variables outside the `execute` function, and all parameters should
be passed by the `param` argument. Also make sure that the return values
generated from `param` function are independent.


## Get task running status

The executor could also implement the optional methods which could get
the task running status.

```python
class CustomExecutor:
    def param(self, vertex):
        return vertex

    def execute(self, param):
        print('Executing:', param)

    def report_start(self, vertice):
        print('Start to run:', vertice)

    def report_running(self, vertice):
        print('Current running:', vertice)

    def report_finish(self, vertice_result):
        for vertex, result in vertice_result:
            print('Finished running {0} with result: {1}'.format(vertex, result))

dag_run(dag, processor=MultiThreadProcessor(), executor=CustomExecutor())
```


## Deliver result to descendants

In case the result for one task should be used for its descendants,
`deliver` method could be implemented in executor.

```python
class CustomExecutor:
    def __init__(self):
        self.__level = {}

    def param(self, vertex):
        return (vertex, self.__level.get(vertex, 0))

    def execute(self, param):
        return param[1] + 1

    def report_finish(self, vertice_result):
        for vertex, result in vertice_result:
            print('Vertex {0} finished, level: {1}'.format(vertex, result))

    def deliver(self, vertex, result):
        self.__level[vertex] = result
```

The result from parent will be delivered to the vertex before execution.


## Topological sorting

[Topological sorting](https://en.wikipedia.org/wiki/Topological_sorting)
could also be done by `paradag.dag_run` function.
The return value of `dag_run` could be considered as
the result of topological sorting.

A simple topological sorting without any execution:

```python
dag = DAG()
dag.add_vertex(1, 2, 3, 4, 5)
dag.add_edge(1, 4)
dag.add_edge(4, 2, 5)

print(dag_run(dag))
print(dag_run(dag, selector=SingleSelector()))
print(dag_run(dag, selector=RandomSelector()))
print(dag_run(dag, selector=ShuffleSelector()))
```

The solution for topological sorting is not necessarily unique,
and the final orders may vary with different selectors.
