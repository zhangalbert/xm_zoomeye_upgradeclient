#! -*- coding: utf-8 -*-


import json


class Notify(object):
    def __init__(self, medias=None, crontab=None):
        self.medias = medias
        self.crontab = crontab

    def get_medias(self):
        return self.medias

    def set_medias(self, medias):
        self.medias = medias

    def get_crontab(self):
        return self.crontab

    def set_crontab(self, crontab):
        self.crontab = crontab

    def to_dict(self):
        dict_data = {
            'medias': map(lambda s: s.to_dict(), self.get_medias()),
            'crontab': self.get_crontab()
        }

        return dict_data

    def to_json(self):
        json_data = json.dumps(self.to_dict())

        return json_data

    @staticmethod
    def from_json(json_data):
        dict_data = json.loads(json_data)

        medias = dict_data.get('medias', None)
        crontab = dict_data.get('crontab', None)

        notify = Notify(medias=medias, crontab=crontab)

        return notify
