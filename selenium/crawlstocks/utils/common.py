#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time

# 装饰器:单实例1
def singleton(cls, *args, **kwargs):
    _instance = {}
    def _wrapper():
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return _wrapper

# 装饰器:单实例2
class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self, *args, **kwargs):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(*args, **kwargs)
        return self._instance[self._cls]

def trycall(func, maxcnt = 6):
    while maxcnt > 0:
        try:
            return func()
        except:
            time.sleep(1)
            maxcnt -= 1
