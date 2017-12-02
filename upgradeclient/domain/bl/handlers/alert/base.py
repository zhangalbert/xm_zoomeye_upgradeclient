#! -*- coding: utf-8 -*-


import os
import json
import datetime


from upgradeclient.database.database import db
from upgradeclient.domain.common.file import File
from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.common.helper import Helper
from upgradeclient.domain.common.crontab import CronTab


logger = Logger.get_logger(__name__)


class BaseHandler(object):
    def __init__(self, conf_path=None):
        self.conf_path = conf_path

    def insert_to_db(self, **kwargs):
        kwargs.update({'log_class': self.__class__.__name__})

        today = datetime.datetime.now().strftime('%Y-%m-%d')

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

    def delete(self, *files):
        for f in files:
            if not os.path.exists(f):
                continue
            os.remove(f)

    def validate(self, obj):
        raise NotImplementedError

    def handle(self, name, crontab, obj):
        raise NotImplementedError

    def timer_generator(self, crontab):
        entry = CronTab(crontab)

        return entry

    def get_conf_dict(self, obj):
        conf_dict = {}
        relation_name = obj.get_relation_name()
        relation_type = obj.get_relation_type()
        try:
            json_data = File.read_content(self.conf_path)
            dict_data = json.loads(json_data)
            conf_dict = dict_data[relation_name][relation_type]
        except Exception as e:
            fmtdata = (self.__class__.__name__, e)
            msgdata = '{0} load configure with exception, exp={1}'.format(*fmtdata)
            logger.error(msgdata)

        return conf_dict


