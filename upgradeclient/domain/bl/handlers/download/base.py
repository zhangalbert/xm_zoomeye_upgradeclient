#! -*- coding: utf-8 -*-


import os
import datetime


from functools import partial
from upgradeclient.database.database import db


class BaseHandler(object):
    def __init__(self, cache=None, dao_factory=None):
        self.cache = cache
        self.dao_factory = dao_factory
        self.event_type = None

    def insert(self, obj):
        parted_dict = {
            'log_name': self.event_type,
            'log_class': self.__class__.__name__,
            'dao_name': obj.get_daoname() or '',
            'file_type': obj.get_filetype() or '',
            'file_name': obj.get_filename() or '',
            'file_url': obj.get_download_url() or '',
            'last_author': obj.get_author() or '',
            'last_date': obj.get_date() or '',
            'last_revision': obj.get_number() or '',
            'last_action': obj.get_action() or '',
        }

        # 删除今日重复插入的内容
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        when_con = 'strftime(\'%Y-%m-%d\', created_time)=\'{0}\''.format(today)
        istorage = partial(db.select)(where=when_con, vars=parted_dict)
        if istorage.first() is None:
            return partial(db.insert, **parted_dict)
        else:
            return partial(db.update, where='{0} and id=\'{1}\''.format(when_con, istorage.first().id), **parted_dict)

    def delete(self, *files):
        for f in files:
            if not os.path.exists(f):
                continue
            os.remove(f)

    def handle(self, obj):
        raise NotImplementedError
