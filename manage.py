#! -*- coding: utf-8 -*-


import os
import sys
import traceback
import logging.config

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from springpython.config import YamlConfig
from springpython.context import ApplicationContext
from upgradeclient.database.database import Database
from upgradeclient.domain.common.logger import Logger


class Client(object):
    """ 从YAML中的XmZoomeyeUpgradeClient对象入口启动

    1. 后期需要后台运行的,可以将父类对象object替换为Daemon即可,run方法已实现
    """
    NAME = 'xm_zoomeye_upgradeclient'
    RELEASE = '1.0.0'

    def __init__(self):
        client_path = Database.get_client_dir()
        log_conf = '_'.join([self.NAME, 'logging.ini'])
        log_path = os.path.join(client_path, 'conf', log_conf)
        logging.config.fileConfig(log_path)

        project_path = Database.get_project_dir()
        self.logger = Logger.get_logger(__name__)
        self.pid_file = '/tmp/upgradeclient/{0}.pid'.format(self.NAME)
        self.out_file = '/tmp/upgradeclient/{0}.out'.format(self.NAME)
        self.err_file = '/tmp/upgradeclient/{0}.err'.format(self.NAME)
        self.ctx_yaml = os.path.join(project_path, '{0}.yaml'.format(self.NAME))

    def logging(self):
        self.logger.debug('*{0} {1}*'.format(self.NAME, self.RELEASE))
        self.logger.debug('ctx_yaml={0}'.format(self.ctx_yaml))
        self.logger.debug('pid_file={0}'.format(self.pid_file))
        self.logger.debug('out_file={0}'.format(self.out_file))
        self.logger.debug('err_file={0}'.format(self.err_file))

    def run(self):
        self.logging()
        try:
            context = ApplicationContext(YamlConfig(self.ctx_yaml))
            service = context.get_object('XmZoomeyeUpgradeClient')
            service.start()
        except Exception as e:
            self.logger.error('resolve yaml context with exception, exp={0}'.format(e))
            self.logger.error(traceback.format_exc())


if __name__ == '__main__':
    client = Client()
    client.run()
