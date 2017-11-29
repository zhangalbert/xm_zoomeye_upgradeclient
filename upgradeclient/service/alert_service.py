#! -*- coding: utf-8 -*-

from threading import Thread
from upgradeclient.domain.common.logger import Logger
from upgradeclient.service.base_service import BaseService


logger = Logger.get_logger(__name__)


class AlertHandlerThread(Thread):
    def __init__(self, obj, service):
        super(AlertHandlerThread, self).__init__()
        self.obj = obj
        self.service = service

    def run(self):
        ins = self.obj.get_data()
        if ins.get_notify() is None:
            fmtdata = (self.__class__.__name__, ins.NAME)
            msgdata = '{0} no notify config for {1}, ignore'.format(*fmtdata)
            logger.error(msgdata)
            return
        logger.error(ins.to_dict())
        self.service.handle(ins)


class AlertService(BaseService):
    def __init__(self, dao_factory=None, alert_factory=None):
        self.dao_factory = dao_factory
        self.alert_factory = alert_factory

    def start(self):
        for name in self.dao_factory:
            dao = self.dao_factory[name]
            t = AlertHandlerThread(dao, self)
            t.daemon = True
            t.start()

    def handle(self, ins):
        notify = ins.get_notify()
        medias = notify.get_medias()
        crontab = notify.get_crontab()
        for media in medias:
            handler = self.alert_factory.create_alert_handler(media)
            t = Thread(target=handler.handle, args=(media.get_handler(), crontab, media))
            t.setDaemon(True)
            t.start()




