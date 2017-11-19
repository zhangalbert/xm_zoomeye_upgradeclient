#! -*- coding: utf-8 -*-


from upgradeclient.domain.model.check.xmjp import XMJP
from upgradeclient.domain.dao.base_dao import BaseDao


class XmjpDao(BaseDao):
    def __init__(self, conf_path=None):
        super(XmjpDao, self).__init__(conf_path=conf_path)

    def get_data(self):
        json_data = self.get_json_data()

        return XMJP.from_json(json_data)

