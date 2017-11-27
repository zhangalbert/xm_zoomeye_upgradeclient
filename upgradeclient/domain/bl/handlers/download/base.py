#! -*- coding: utf-8 -*-


import os
import datetime


from upgradeclient.database.database import db
from upgradeclient.domain.common.helper import Helper


class BaseHandler(object):
    def __init__(self, cache=None, dao_factory=None):
        self.cache = cache
        self.dao_factory = dao_factory
        self.event_type = None

    def insert_to_db(self, obj, **kwargs):
        kwargs.update({
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
        })

        today = datetime.datetime.now().strftime('%Y-%m-%d')

        select_where_condition = ' '.join(Helper.combin_sql_conditions(s='and', **kwargs))
        select_command = [
            'select id',
            'from upgradeclient',
            'where {0} and strftime(\'%Y-%m-%d\', created_time)=\'{1}\''.format(select_where_condition, today)
        ]
        insert_command = [
            'INSERT INTO upgradeclient',
            '({0})'.format(','.join(kwargs.keys())),
            'values ({0})'.format(','.join(Helper.combin_sql_values(kwargs.values())))
        ]
        select_res = db.select_one(' '.join(select_command))
        if select_res is None:
            db.execute(' '.join(insert_command))
            return
        update_where_condition = Helper.combin_sql_conditions(s='and', id=select_res[0])
        update_command = [
            'update upgradeclient',
            'set created_time=\'{0}\',{1}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                  ','.join(Helper.combin_sql_conditions(s='', **kwargs))),
            'where {0}'.format(' '.join(update_where_condition))
        ]
        db.execute(' '.join(update_command))

    def delete(self, *files):
        for f in files:
            if not os.path.exists(f):
                continue
            os.remove(f)

    def handle(self, obj):
        raise NotImplementedError
