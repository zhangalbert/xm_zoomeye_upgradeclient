#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class DownloadHandlerFactory(object):
    def __init__(self, download_handlers=None):
        self.download_handlers = download_handlers

    def create_download_handler(self, obj):
        logger.debug('download handler factory create download handler ... ')
        handler_name = obj.get_name().lower() if obj.get_name() else 'UnknowHandler'
        if handler_name not in self.download_handlers:
            logger.debug('invalid event, no download handler matched(use default), name={0}'.format(handler_name))
            download_handler = self.download_handlers['default']
        else:
            download_handler = self.download_handlers[handler_name]

        return download_handler




