#! -*- coding: utf-8 *-


import json


class Media(object):
    def __init__(self, handler=None, to=None, cc=None):
        self.to = to
        self.cc = to
        self.handler = handler

    def get_to(self):
        return self.to

    def set_to(self, to):
        self.to = to

    def get_cc(self):
        return self.cc

    def set_cc(self, cc):
        self.cc = cc

    def get_handler(self):
        return self.handler

    def set_handler(self, handler):
        self.handler = handler

    def to_dict(self):
        dict_data = {
            'to': self.get_to(),
            'cc': self.get_cc(),
            'handler': self.get_handler()
        }

        return dict_data

    def to_json(self):
        dict_data = self.to_dict()
        json_data = json.dumps(dict_data)

        return json_data

    @staticmethod
    def from_json(json_data):
        dict_data = json.loads(json_data)

        to = dict_data.get('to', None)
        cc = dict_data.get('cc', None)
        handler = dict_data.get('handler', None)

        media = Media(handler=handler, to=to, cc=cc)

        return media
