#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.bl.handlers.alert.base import BaseHandler


logger = Logger.get_logger(__name__)


class DefaultHandler(BaseHandler):
    def __init__(self, conf_path=None):
        super(DefaultHandler, self).__init__(conf_path)

    def validate(self, obj):
        pass

    def handle(self, name, crontab, obj):
        fmtdata = (self.__class__.__name__, obj.to_json())
        logger.info('{0} handled the invalid event, data={1}'.format(*fmtdata))


