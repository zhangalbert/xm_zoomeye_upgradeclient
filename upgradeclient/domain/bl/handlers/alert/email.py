#! -*- coding: utf-8 -*-


import time
import json
import sched
import datetime
import traceback


from upgradeclient.database.database import db
from upgradeclient.domain.common.file import File
from upgradeclient.domain.common.mail import Email
from upgradeclient.domain.common.filter import Q, R
from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.bl.handlers.alert.base import BaseHandler


logger = Logger.get_logger(__name__)


class EmailHandler(BaseHandler):
    def __init__(self, conf_path=None):
        super(EmailHandler, self).__init__(conf_path)

    def validate(self, obj):
        q = Q(obj__smtp_host__not_exact='') & \
            Q(obj__smtp_port__not_exact='') & \
            Q(obj__smtp_user__not_exact='') & \
            Q(obj__smtp_pass__not_exact='') & \
            Q(obj__debug_num__not_exact='')

        return R(obj, q_ins=q)

    def handle(self, name, crontab, obj):
        t = self.timer_generator(crontab)
        s = sched.scheduler(time.time, time.sleep)
        while True:
            s.enter(t.next(), 1, self.report_hook, (name, obj,))
            s.run()

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
        for ins in select_results:
            res_data.append(ins)

        return res_data

    def get_html(self, data):

        html = '<ul>'
        for d in data:
            html += '<li>'
            html += 'version: {0} # '.format(d[-4])
            html += 'error: {0} # '.format(d[-2])
            html += '<a href="http://10.2.5.51:8081/firmware/{0}">detail</a>'.format(d[0])
            html += '</li>'
        html += '</ul>'

        return html

    def report_hook(self, name, obj):
        data = self.get_data(name)
        if not data:
            logger.warning('{0} get no abnormal data, ignore, wait next scheduler')
            return
        html = self.get_html(data)

        dict_conf = self.get_conf_dict(obj)
        tobj = type('tobj', (object,), dict_conf or {})
        if not self.validate(tobj):
            fmtdata = (self.__class__.__name__,)
            msgdata = '{0} load invalid conf (smtp_host,smtp_port,smtp_user,smtp_pass,debug_num)'.format(*fmtdata)
            logger.error(msgdata)
            return

        email_res = Email.send(dict_conf,
                               u'云产品线-固件上传异常检测: 近日{0}自动升级异常检测结果'.format(name.upper()),
                               obj.get_to(), ecc=obj.get_cc(), ehtml=html)

        if email_res['is_success'] is False:
            fmtdata = (self.__class__, email_res['error'])
            msgdata = '{0} send mail with exception, exp={1}'.format(*fmtdata)
            logger.error(msgdata)
            self.insert_to_db(log_level='error ',  log_message=msgdata)


