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
        res_data = select_results

        return res_data

    def load_config(self):
        dict_data = {}
        try:
            jtxt_data = File.read_content(self.conf_path)
            dict_data = json.loads(jtxt_data)
        except Exception as e:
            fmtdata = (self.__class__.__name__, e)
            msgdata = '{0} load config with exception, exp={0}'.format(*fmtdata)
            logger.error(msgdata)
            logger.error(traceback.format_exc())

        return dict_data

    def get_html(self, data):

        html = '<ul>'
        for d in data:
            html += '<li>' + d[-2] + '</li>'
        html += '</ul>'

        return html

    def report_hook(self, name, obj):
        data = self.get_data(name)
        if not data:
            logger.warning('{0} get no abnormal data, ignore, wait next scheduler')
            return
        html = self.get_html(data)

        dict_conf = self.load_config()
        mail_conf = dict_conf.get('email', None)
        obj = type('obj', (object,), mail_conf or {})
        if not self.validate(obj):
            fmtdata = (self.__class__.__name__,)
            msgdata = '{0} load invalid conf (smtp_host,smtp_port,smtp_user,smtp_pass,debug_num)'.format(*fmtdata)
            logger.error(msgdata)
            return

        email_res = Email.send(mail_conf,
                               u'云产品线-固件上传异常检测: 近日{0}自动升级异常检测结果'.format(name.upper()),
                               obj.get_to() or ['limanman@xiongmaitech.com'], ecc=obj.get_cc(), ehtml=html)
        if email_res['is_success'] is False:
            fmtdata = (self.__class__, email_res['error'])
            msgdata = '{0} send mail with exception, exp={1}'.format(*fmtdata)
            logger.error(msgdata)
            self.insert_to_db(log_level='error ',  log_message=msgdata)

