#!/usr/bin/env python
#-*- coding:utf-8 -*-

from functools import wraps

class DecorateClass(object):
    """
        Base class for decorator
    """
    def decorate(self):
        for name, fn in self.iter():
            if not self.filter(name, fn):
                continue
            self.operate(name, fn)


class MethodDecorator(DecorateClass):
    """
        FuncDecorator used to add a wrapper for each method of the class
        Do what you like in your custom function
        Wrapper function should return a function that accept (*args, **kwargs)
        and pass them to inner method it wraps
    """
    def __init__(self, obj, wrapper):
        self._obj = obj
        self._wrapper = wrapper 
        DecorateClass.__init__(self)

    def iter(self):
        return [(name, getattr(self._obj, name)) for name in dir(self._obj)]

    def filter(self, name, fn):
        if not name.startswith('_') and callable(fn):
            return True
        else:
            return False

    def operate(self, name, fn):
        setattr(self._obj, name, self._wrapper(fn))


def args_to_str(*argv):
    try:
        return '>>>args:' + str(argv)
    except Exception, e:
        return 'trans args to string failed.' + str(e)


def args_logger(fn, logger):
    @wraps(fn)
    def _(self, *args, **kwargs):
        logger.info(fn.__name__ + ' is called\n' + args_to_str(args))
        return fn(self, *args, **kwargs)
    return _
