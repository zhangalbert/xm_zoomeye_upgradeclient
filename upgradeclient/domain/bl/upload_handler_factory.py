#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class UploadHandlerFactory(object):
    def __init__(self, upload_handlers=None):
        self.upload_handlers = upload_handlers

    def create_upload_handler(self, handler_name='default'):
        fmtdata = (self.__class__.__name__,)
        logger.debug('{0} create upload handler ... '.format(*fmtdata))

        if handler_name not in self.upload_handlers:
            fmtdata = (self.__class__.__name__, handler_name)
            logger.error('{0} recv invalid download name (no handler matched) use default, name={1}'.format(*fmtdata))
            upload_handler = self.upload_handlers['default']
        else:
            upload_handler = self.upload_handlers[handler_name]

        return upload_handler



