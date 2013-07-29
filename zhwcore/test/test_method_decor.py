from __future__ import absolute_import

from zhwcore.common.method_decor import MethodDecorator

def t_wrapper(f):
    def _(self, *argv, **kwargs):
        return f(self, *argv, **kwargs) + 1
    return _

class T(object):
    def __init__(self):
        MethodDecorator(self, t_wrapper).decorate()

    def add(self, a, b):
        return a+b

class TestCaseMethodDecorator(object):
    def __init__(self):
        pass

    def test_wrapper(self):
        assert T().add(1,2) == 4
