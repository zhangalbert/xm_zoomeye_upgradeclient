#! -*- coding: utf-8 -*-


from upgradeclient.domain.dao.base_dao import BaseDao
from upgradeclient.domain.model.check.check import Check


class CheckDao(BaseDao):
    def __init__(self, conf_path=None):
        super(CheckDao, self).__init__(conf_path=conf_path)

    def get_data(self):
        json_data = self.get_json_data()

        return Check.from_json(json_data)

