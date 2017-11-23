#! -*- coding: utf-8 -*-


import os


class BaseHandler(object):
    def __init__(self, cache=None):
        self.cache = cache

    def delete(self, *files):
        for f in files:
            if not os.path.exists(f):
                continue
            os.remove(f)

    def handle(self, obj):
        raise NotImplementedError
