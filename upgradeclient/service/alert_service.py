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
        if ins.get_alert() is None:
            fmtdata = (self.__class__.__name__, ins.get_name())
            msgdata = '{0} detected no alert config for {1}, ignore'.format(*fmtdata)
            logger.warning(msgdata)
            return
        self.service.handle(ins)


class AlertService(BaseService):
    def __init__(self, dao_factory=None, handler_factory=None):
        self.dao_factory = dao_factory
        self.handler_factory = handler_factory

    def pre_start(self):
        pass

    def post_start(self):
        pass

    def start(self):
        for name in self.dao_factory.check_daos:
            dao = self.dao_factory.create_check_dao(name)
            t = AlertHandlerThread(dao, self)
            t.daemon = True
            t.start()

    def handle(self, ins):
        alerts = ins.get_alert()
        medias = alerts.get_medias()
        crontab = alerts.get_crontab()
        for media in medias:
            handler_name = media.get_relation_type()
            handler = self.handler_factory.create_alert_handler(handler_name)
            t = Thread(target=handler.handle, args=(ins.get_name(), crontab, media))
            t.setDaemon(True)
            t.start()




