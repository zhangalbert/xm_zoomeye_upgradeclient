#! -*- coding: utf-8 -*-


import time
import sched


from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.common.crontab import CronTab
from upgradeclient.domain.bl.handlers.alert.base import BaseHandler

logger = Logger.get_logger(__name__)


class EmailHandler(BaseHandler):
    def __init__(self, conf_path=None):
        super(EmailHandler, self).__init__(conf_path)

    def handle(self, obj):
        t = self.generate_timer(obj)
        while True:
            s = sched.scheduler(time.time, time.sleep)
            s.enter(t.next(), 1, self.report_hook, (obj,))

    def generate_timer(self, obj):
        notify = obj.get_notify()
        crontab = notify.get_crontab()
        entry = CronTab(crontab)

        return entry

    def report_hook(self, obj):
        print 'X' * 100
        print 'I was running~'
        print 'X' * 100
