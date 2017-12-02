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
    a 已经下载的数据块
    b 数据块的大小
    c 远程文件大小
    """
    percent = min(100.0 * a * b / c, 100)
    fmtdata = (cls.__class__.__name__, threading.currentThread().name, cls.filename, percent)
    msgdata = '{0} thread {1} download {2} {3:.2f}%/100%'.format(*fmtdata)
    logger.debug(msgdata)


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
        return_res = {'is_success': True, 'error': ''}

        self.url, self.filename = url, filename
        download_fname = '{0}.downloading'.format(filename)

        fmtdata = (self.__class__.__name__, threading.currentThread().name, filename, url)
        msgdata = '{0} thread {1} start download {2} from {3}'.format(*fmtdata)
        logger.info(msgdata)
        try:
            urllib.urlretrieve(url, filename=download_fname, reporthook=self.reporthook, *kwargs)
            shutil.move(download_fname, filename)
            fmtdata = (self.__class__.__name__, threading.currentThread().name, filename, url)
            msgdata = '{0} thread {1} download {2} from {3} success'.format(*fmtdata)
            logger.info(msgdata)
        except Exception as e:
            fmtdata = (self.__class__.__name__, threading.currentThread().name, filename, url, e)
            msgdata = '{0} thread {1} download {2} from {3} with exception, exp={4}'.format(*fmtdata)
            logger.error(msgdata)
            return_res = {'is_success': False, 'error': e}
        finally:
            os.path.exists(download_fname) and os.remove(download_fname)

        return return_res

