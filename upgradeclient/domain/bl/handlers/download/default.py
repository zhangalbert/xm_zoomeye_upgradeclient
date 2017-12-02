#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.bl.handlers.download.base import BaseHandler


logger = Logger.get_logger(__name__)


class DefaultHandler(BaseHandler):
    def handle(self, obj):
        fmtdata = (self.__class__.__name__, obj.to_json())
        logger.info('{0} handled the invalid download event, data={1}'.format(*fmtdata))
