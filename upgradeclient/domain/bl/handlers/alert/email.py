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

    def handle(self, crontab, obj):
        t = self.__class__.timer_generator(crontab)
        while True:
            s = sched.scheduler(time.time, time.sleep)
            s.enter(t.next(), 1, self.__class__.report_hook, (obj,))

    @staticmethod
    def timer_generator(crontab):
        entry = CronTab(crontab)

        return entry

    @staticmethod
    def report_hook(obj):
        print 'X' * 100
        print 'I was running~'
        print 'X' * 100
