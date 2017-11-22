#! -*- coding: utf-8 -*-


import os
import urllib
import shutil
import threading


from functools import partial
from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


def reporthook(cls, a, b, c):
    """
    1. a 已经下载的数据块
    2. b 数据块的大小
    3. c 远程文件大小
    """
    percent = min(100.0 * a * b / c, 100)
    logger.info('{0} download {1} {2}%/100%'.format(threading.currentThread(), cls.filename, percent))


class Download(object):
    def __init__(self):
        self.url = None
        self.filename = None
        self.reporthook = partial(reporthook, self)

    def reg_reporthook(self, func=None):
        if callable(func):
            self.reporthook = func
            return

    def wget(self, url, filename, **kwargs):
        is_success = True

        self.url, self.filename = url, filename
        download_fname = '{0}.downloading'.format(filename)

        logger.info('start download {0} from {1}'.format(filename, url))
        try:
            urllib.urlretrieve(url, filename=download_fname, reporthook=self.reporthook, *kwargs)
            shutil.move(download_fname, filename)
            logger.info('download {0} from {1} successfuly'.format(filename, url))
        except Exception as e:
            is_success = False
            logger.error('download {0} from {1} with exception, exp={2}'.format(filename, url, e))
        finally:
            os.path.exists(download_fname) and os.remove(download_fname)
        return is_success


