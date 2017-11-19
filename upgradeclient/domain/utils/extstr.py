#! -*- coding: utf-8 -*-


import re


class ExtStr(str):
    def __init__(self, *args, **kwargs):
        super(ExtStr, self).__init__()

    def exact(self, data):
        return self == data

    def iexact(self, data):
        return self.lower() == data.lower()

    def contains(self, data):
        return data in self

    def icontains(self, data):
        return data.lower() in self.lower()

    def istartswith(self, data):
        return self.lower().startswith(data.lower())

    def iendswith(self, data):
        return self.lower().endswith(data.lower())

    def regexp(self, data):
        return re.search(data, self)



