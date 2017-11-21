#! -*- coding: utf-8 -*-


class BaseHandler(object):
    def __init__(self, cache=None, dao_factory=None):
        self.cache = cache
        self.dao_factory = dao_factory

    def handle(self, obj):
        raise NotImplementedError
