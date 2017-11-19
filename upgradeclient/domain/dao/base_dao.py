#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.file import File


class BaseDao(object):
    def __init__(self, conf_path=None):
        self.conf_path = conf_path

    def get_json_data(self):
        json_data = File.read_content(self.conf_path)

        return json_data

    def get_data(self):
        raise NotImplementedError
