#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class AlertHandlerFactory(object):
    def __init__(self, alert_handlers=None):
        self.alert_handlers = alert_handlers

    def create_alert_handler(self, handler_name):
        fmtdata = (self.__class__.__name__,)
        logger.debug('{0} create alert handler ... '.format(*fmtdata))

        if handler_name not in self.alert_handlers:
            fmtdata = (self.__class__.__name__, handler_name)
            logger.error('{0} recv invalid alert name (no handler matched) use default, name={1}'.format(*fmtdata))
            alert_handler = self.alert_handlers['default']
        else:
            alert_handler = self.alert_handlers[handler_name]

        return alert_handler
