#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class DownloadHandlerFactory(object):
    def __init__(self, download_handlers=None):
        self.download_handlers = download_handlers

    def create_download_handler(self, obj):
        fmtdata = (self.__class__.__name__,)
        logger.debug('{0} create download handler ... '.format(*fmtdata))
        handler_name = obj.get_name().lower() if obj.get_name() else 'UnknowHandler'

        if handler_name not in self.download_handlers:
            fmtdata = (self.__class__.__name__, handler_name)
            logger.error('{0} recv invalid event (no handler matched) use default, name={1}'.format(*fmtdata))
            download_handler = self.download_handlers['default']
        else:
            download_handler = self.download_handlers[handler_name]

        return download_handler




