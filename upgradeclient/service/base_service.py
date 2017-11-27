#! -*- coding: utf-8 -*-


import datetime

from functools import partial
from upgradeclient.database.database import db


class BaseService(object):
    def insert(self):
        parted_dict = {
            'log_class': self.__class__.__name__,
        }
        # 删除今日重复插入的内容
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        when_con = 'strftime(\'%Y-%m-%d\', created_time)=\'{0}\''.format(today)
        istorage = partial(db.select)(where=when_con, vars=parted_dict)
        if istorage.first() is None:
            return partial(db.insert, **parted_dict)
        else:
            return partial(db.update, where='{0},id=\'{1}\''.format(when_con, istorage.first().id), **parted_dict)
