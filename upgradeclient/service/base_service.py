#! -*- coding: utf-8 -*-


import datetime


from upgradeclient.database.database import db
from upgradeclient.domain.common.helper import Helper


class BaseService(object):
    def insert_to_db(self, **kwargs):
        kwargs.update({'log_class': self.__class__.__name__})
        today = datetime.datetime.now().strftime('%Y-%m-%d')

        kwargs['log_message'] = Helper.string_escape(kwargs['log_message'])

        select_where_condition = ' '.join(Helper.combin_sql_conditions('and', kwargs.items()))
        select_command = [
            'select id',
            'from upgradeclient',
            'where {0} and strftime(\'%Y-%m-%d\', created_time)=\'{1}\''.format(select_where_condition, today)
        ]
        insert_command = [
            'INSERT INTO upgradeclient',
            '({0})'.format(','.join(kwargs.keys())),
            'values ({0})'.format(','.join(Helper.combin_sql_values(*kwargs.values())))
        ]
        select_res = db.select_one(' '.join(select_command))
        if select_res is None:
            db.execute(' '.join(insert_command))
            return
        update_where_condition = Helper.combin_sql_conditions('and', [('id', select_res[0])])
        update_command = [
            'update upgradeclient',
            'set created_time=\'{0}\',{1}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                  ','.join(Helper.combin_sql_conditions('', kwargs.items()))),
            'where {0}'.format(' '.join(update_where_condition))
        ]
        db.execute(' '.join(update_command))

    def start(self):
        raise NotImplementedError

    def pre_start(self):
        raise NotImplementedError

    def post_start(self):
        raise NotImplementedError
