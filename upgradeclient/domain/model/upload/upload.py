#! -*- coding: utf-8 -*-


import json


class Upload(object):
    def __init__(self, relation_name=None, relation_type=None):
        self.relation_name = relation_name
        self.relation_type = relation_type

    def get_relation_name(self):
        return self.relation_name

    def set_relation_name(self, relation_name):
        self.relation_name = relation_name

    def get_relation_type(self):
        return self.relation_type

    def set_relation_type(self, relation_type):
        self.relation_type = relation_type

    def to_dict(self):
        dict_data = {
            'relation_name': self.get_relation_name(),
            'relation_type': self.get_relation_type()
        }

        return dict_data

    def to_json(self, indent=4):
        dict_data = self.to_dict()
        json_data = json.dumps(dict_data, indent=indent)

        return json_data

    @staticmethod
    def from_json(json_data):
        dict_data = json.loads(json_data)

        relation_name = dict_data.get('relation_name', None)
        relation_type = dict_data.get('relation_type', None)

        upload = Upload(relation_name=relation_name, relation_type=relation_type)

        return upload

