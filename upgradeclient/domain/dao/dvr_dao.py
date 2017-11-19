#! -*- coding: utf-8 -*-


from upgradeclient.domain.model.check.dvr import DVR
from upgradeclient.domain.dao.base_dao import BaseDao


class DvrDao(BaseDao):
    def __init__(self, conf_path=None):
        super(DvrDao, self).__init__(conf_path=conf_path)

    def get_data(self):
        json_data = self.get_json_data()

        return DVR.from_json(json_data)
