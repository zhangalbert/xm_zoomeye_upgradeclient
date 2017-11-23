#! -*- coding: utf-8 -*-


from upgradeclient.domain.dao.base_dao import BaseDao
from upgradeclient.domain.model.upload.rsync import Rsync


class RsyncDao(BaseDao):
    def __init__(self, conf_path=None):
        super(RsyncDao, self).__init__(conf_path=conf_path)

    def get_data(self):
        json_data = self.get_json_data()

        return Rsync.from_json(json_data)


