#! -*- coding: utf-8 -*-


import os


class BaseHandler(object):
    def __init__(self, cache=None, dao_factory=None):
        self.cache = cache
        self.dao_factory = dao_factory

    def delete(self, *files):
        for f in files:
            if not os.path.exists(f):
                continue
            os.remove(f)

    def handle(self, obj):
        raise NotImplementedError

