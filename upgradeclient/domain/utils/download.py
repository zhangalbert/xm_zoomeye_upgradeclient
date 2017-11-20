#! -*- coding: utf-8 -*-


import os
import urllib
import shutil
import threading


from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class Download(object):
    def __init__(self):
        self._url = None
        self._filename = None
        self._wrapped_reporthook = None

    def _reporthook(self, a, b, c):
        """
        1. a 已经下载的数据块
        2. b 数据块的大小
        3. c 远程文件大小
        """
        if self._wrapped_reporthook and isinstance(self._wrapped_reporthook, function):
            self._wrapped_reporthook(self, a, b, c)

    def _defaulthook(self, cls, a, b, c):
        percent = min(100.0 * a * b / c, 100)
        logger.info('{0} download {1} {2}%/100%'.format(threading.currentThread(), cls._filename, percent))

    def reg_reporthook(self, callback=None):
        self._wrapped_reporthook = callback or self._defaulthook

    def wget(self, url, filename, **kwargs):
        self._url, self._filename = url, filename
        download_fname = '{0}.downloading'.format(filename)

        logger.info('start download {0} from {1}'.format(filename, url))
        try:
            urllib.urlretrieve(url, filename=download_fname, reporthook=self._reporthook, *kwargs)
            shutil.move(download_fname, filename)
            logger.info('download {0} from {1} successfuly'.format(filename, url))
        except Exception as e:
            logger.error('download {0} from {1} with exception, exp={2}'.format(filename, url, e))
        finally:
            if os.path.exists(download_fname):
                os.remove(download_fname)


