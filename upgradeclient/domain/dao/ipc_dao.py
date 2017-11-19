#! -*- coding: utf-8 -*-


from upgradeclient.domain.model.check.ipc import IPC
from upgradeclient.domain.dao.base_dao import BaseDao


class IpcDao(BaseDao):
    def __init__(self, conf_path=None):
        super(IpcDao, self).__init__(conf_path=conf_path)

    def get_data(self):
        json_data = self.get_json_data()

        return IPC.from_json(json_data)
