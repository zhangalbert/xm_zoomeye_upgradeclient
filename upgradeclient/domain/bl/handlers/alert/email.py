#! -*- coding: utf-8 -*-


import time
import json
import sched
import datetime


from upgradeclient.database.database import db
from upgradeclient.domain.common.file import File
from upgradeclient.domain.common.mail import Email
from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.common.crontab import CronTab
from upgradeclient.domain.bl.handlers.alert.base import BaseHandler

logger = Logger.get_logger(__name__)


class EmailHandler(BaseHandler):
    def __init__(self, conf_path=None):
        super(EmailHandler, self).__init__(conf_path)

    def get_data(self, name):
        res_data = []

        today = datetime.datetime.now().strftime('%Y-%m-%d')
        fmtdata = (name, today)
        select_command = [
            'select *',
            'from upgradeclient',
            'where log_level=\'error\' and  dao_name=\'{0}\' and strftime(\'%Y-%m-%d\', created_time)=\'{1}\''.format(
                *fmtdata
            )
        ]
        select_results = db.select(' '.join(select_command))
        if select_results is None:
            return res_data
        res_data = select_results

        return res_data

    def validate(self):
        validate_res = super(EmailHandler, self).validate()

        return validate_res

    def handle(self, name, crontab, obj):
        if self.validate():
            return
        t = self.__class__.timer_generator(crontab)
        while True:
            s = sched.scheduler(time.time, time.sleep)
            ts = t.next()
            print 'next run after seconds: {0}'.format(ts)
            s.enter(ts, 1, self.report_hook, (name, obj,))
            s.run()

    @staticmethod
    def timer_generator(crontab):
        entry = CronTab(crontab)

        return entry

    def load_config(self):
        jtxt_data = File.read_content(self.conf_path)
        dict_data = json.loads(jtxt_data)

        return dict_data

    def get_html(self):
        pass

    def report_hook(self, name, obj):
        data = self.get_data(name)
        html = '<table><thead><tr><td>型号</td><td>异常</td></tr></thead><tbody>'
        for d in data:
            html += '<tr><td>'+d[4]+'</td><td>'+d[-2]+'</td></tr>'
        html += '</tbody></table>'

        print html

        dict_conf = self.load_config()
        if name not in dict_conf:
            return
        mail_conf = dict_conf[name]
        Email.send(mail_conf, '测试邮件', obj.get_to(), ecc=obj.get_cc(), ehtml=html)