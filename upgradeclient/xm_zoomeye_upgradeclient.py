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

    def start(self):
        # if self.download_service is not None and self.download_service != 'None':
        #     logger.info('start download service successfully!')
        #     self.download_service.start()
        #
        # if self.upload_service is not None and self.upload_service != 'None':
        #     logger.info('start upload service successfully!')
        #     self.upload_service.start()
        #
        # if self.alert_service is not None and self.alert_service != 'None':
        #     logger.info('start alert service successfully!')
        #     self.alert_service.start()

        if self.webui_service is not None and self.webui_service != 'None':
            logger.info('start webui service successfully!')
            self.webui_service.start()

        # if self.check_service is not None and self.check_service != 'None':
        #     logger.info('start check service successfully!')
        #     self.check_service.start()


        import time
        while True:
            time.sleep(1)