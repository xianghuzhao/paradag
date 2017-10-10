paradag
=======

.. image:: https://img.shields.io/pypi/v/paradag.svg
   :target: https://pypi.python.org/pypi/paradag
   :alt: PyPI

.. image:: https://travis-ci.org/xianghuzhao/paradag.svg?branch=master
   :target: https://travis-ci.org/xianghuzhao/paradag
   :alt: Travis CI Status

.. image:: https://codeclimate.com/github/xianghuzhao/paradag/badges/gpa.svg
   :target: https://codeclimate.com/github/xianghuzhao/paradag
   :alt: Code Climate

A robust DAG package for easy parallel execution.

paradag is implemented in pure python and totally independent of any
other packages.

Try to make execute as simple as possible. Extra operation could be put
in `report_*` functions, like logging.


Paralell Execution
------------------

It is OK to use `MultiThreadProcessor` if your vertices are running
I/O a lot. Due to GIL, you need `MultiProcessingProcessor` if your
vertices contain CPU consumption parts with python code.

One exception is that if you are running vertices which invoke
subprocesses, it would be OK with `MultiThreadProcessor`.
