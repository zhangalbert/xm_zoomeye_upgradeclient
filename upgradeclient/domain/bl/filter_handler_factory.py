#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class FilterHandlerFactory(object):
    def __init__(self, filter_handlers=None):
        self.filter_handlers = filter_handlers

    def create_filter_handler(self, filter_name='default'):
        fmtdata = (self.__class__.__name__,)
        logger.debug('{0} create filter handler ... '.format(*fmtdata))

        if filter_name not in self.filter_handlers:
            fmtdata = (self.__class__.__name__, filter_name)
            logger.error('{0} recv invalid filter name (no handler matched) use default, name={1}'.format(*fmtdata))
            filter_handler = self.filter_handlers['default']
        else:
            filter_handler = self.filter_handlers[filter_name]

        return filter_handler
