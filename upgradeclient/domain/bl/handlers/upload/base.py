#! -*- coding: utf-8 -*-


import os
import json


from upgradeclient.domain.common.file import File
from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class BaseHandler(object):
    def __init__(self, cache=None, conf_path=None):
        self.cache = cache
        self.conf_path = conf_path

    def delete(self, *files):
        for f in files:
            if not os.path.exists(f):
                continue
            os.remove(f)

    def handle(self, obj):
        raise NotImplementedError

    def get_conf_dict(self, obj):
        conf_dict = {}
        relation_name = obj.get_relation_name()
        relation_type = obj.get_relation_type()
        try:
            json_data = File.read_content(self.conf_path)
            dict_data = json.loads(json_data)
            conf_dict = dict_data[relation_name][relation_type]
        except Exception as e:
            fmtdata = (self.__class__.__name__, e)
            msgdata = '{0} load configure with exception, exp={1}'.format(*fmtdata)
            logger.error(msgdata)

        return conf_dict
