#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class UploadDaoFactory(object):
    def __init__(self, upload_daos=None):
        self.upload_daos = upload_daos

    def create_upload_dao(self, dao_name='default'):
        fmtdata = (self.__class__.__name__,)
        logger.debug('{0} create upload dao ... '.format(*fmtdata))

        if dao_name not in self.upload_daos:
            fmtdata = (self.__class__.__name__, dao_name)
            logger.error('{0} recv invalid upload name (no dao matched) use default, name={1}'.format(*fmtdata))
            upload_dao = self.upload_daos['default']
        else:
            upload_dao = self.upload_daos[dao_name]

        return upload_dao

