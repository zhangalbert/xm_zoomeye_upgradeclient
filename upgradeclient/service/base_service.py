#! -*- coding: utf-8 -*-


from functools import partial
from upgradeclient.database.database import db


class BaseService(object):
    def insert(self):
        parted_dict = {
            'log_class': self.__class__.__name__,
        }

        return partial(db.insert, **parted_dict)
