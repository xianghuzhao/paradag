# paradag

[![PyPI](https://badge.fury.io/py/paradag.svg)](https://pypi.org/project/paradag/)
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

> I DO NOT intend to publish this package to PyPi. Therefore, stable version will be always available on `master` branch.

```shell
pip install -U git+https://github.com/0hsn/paradag.git@master
```

## Usage

Read the [usage docs](docs/usage.md).

Create issue or ask a qustion https://github.com/0hsn/paradag/issues.

Follow the [common convention](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project) for contribuiton
