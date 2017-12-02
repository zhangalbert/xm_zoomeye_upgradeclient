#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class XmZoomeyeUpgradeClient(object):
    def __init__(self, download_service=None, upload_service=None, alert_service=None, check_service=None,
                 webui_service=None):
        self.download_service = download_service
        self.upload_service = upload_service
        self.alert_service = alert_service
        self.check_service = check_service
        self.webui_service = webui_service

    def __run(self, services=[]):
        if not services:
            logger.warning('no service was loaded, ignore')
            return
        for service in services:
            service_obj = getattr(self, service, None)
            if service_obj == 'None' or service_obj is None:
                fmtdata = (self.__class__.__name__, service)
                msgdata = '{0} found service {1} has not been realize'.format(*fmtdata)
                logger.warning(msgdata)
                return
            logger.info('start {0} successfully!'.format(service))
            service_obj.start()

    def start(self):
        # prod:
        self.__run(['download_service', 'upload_service', 'alert_service', 'webui_service', 'check_service'])
