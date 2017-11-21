#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.bl.handlers.base import BaseHandler


logger = Logger.get_logger(__name__)


class DefaultHandler(BaseHandler):
    def handle(self, obj):
        logger.info('{0} handle the invalid data, json={1}'.format(self.__class__.__name__, obj.to_json()))

