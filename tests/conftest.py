import pytest

import datetime

from paradag import Dag


class SimpleCallable(object):
    def __init__(self, val):
        self.__val = val

    def __call__(self):
        self.__call_time = datetime.datetime.now()
        self.__result = self.__val ** 2

    def __str__(self):
        return 'SimpleCallable: {0}'.format(self.__val)

    @property
    def call_time(self):
        return self.__call_time

    @property
    def result(self):
        return self.__result

@pytest.fixture(scope='module')
def dag_callable():
    d = Dag()
    s1 = SimpleCallable(1)
    s2 = SimpleCallable(2)
    s3 = SimpleCallable(3)
    s4 = SimpleCallable(4)
    s5 = SimpleCallable(5)
    d.add_vertex(s1, s2, s3, s4, s5)
    d.add_edge(s1, s2, s3)
    d.add_edge(s2, s4)
    d.add_edge(s3, s4)
    return (d, s1, s2, s3, s4, s5)
