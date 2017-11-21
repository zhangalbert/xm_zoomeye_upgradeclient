#! -*- coding: utf-8 -*-


class BaseHandler(object):
    def __init__(self, cache=None):
        self.cache = cache

    def handle(self, obj):
        raise NotImplementedError
