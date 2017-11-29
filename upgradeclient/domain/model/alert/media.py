#! -*- coding: utf-8 *-


import json


class Media(object):
    def __init__(self, tp=None, to=None, cc=None):
        self.tp = None
        self.to = None
        self.cc = None

    def get_tp(self):
        return self.tp

    def set_tp(self, tp):
        self.tp = tp

    def get_to(self):
        return self.to

    def set_to(self, to):
        self.to = to

    def get_cc(self):
        return self.cc

    def set_cc(self, cc):
        self.cc = cc

    def to_dict(self):
        dict_data = {
            self.get_tp(): {
                'to': self.get_to(),
                'cc': self.get_cc(),
            }
        }

        return dict_data

    def to_json(self):
        dict_data = self.to_dict()
        json_data = json.dumps(dict_data)

        return json_data

    @staticmethod
    def from_json(json_data):
        dict_data = json.loads(json_data)

        tp = dict_data.get('tp', None)
        to = dict_data.get('to', None)
        cc = dict_data.get('cc', None)

        media = Media(tp=tp, to=to, cc=cc)

        return media
