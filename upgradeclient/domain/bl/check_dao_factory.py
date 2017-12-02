#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class CheckDaoFactory(object):
    def __init__(self, check_daos=None):
        self.check_daos = check_daos

    def create_check_dao(self, dao_name='default'):
        fmtdata = (self.__class__.__name__,)
        logger.debug('{0} create check dao ... '.format(*fmtdata))

        if dao_name not in self.check_daos:
            fmtdata = (self.__class__.__name__, dao_name)
            logger.error('{0} recv invalid check name (no dao matched) use default, name={1}'.format(*fmtdata))
            check_dao = self.check_daos['default']
        else:
            check_dao = self.check_daos[dao_name]

        return check_dao
