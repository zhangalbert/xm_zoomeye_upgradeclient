#! -*- coding: utf-8 -*-


import os


from upgradeclient.domain.common.file import File
from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class Cache(object):
    def __init__(self, base_rpath=None, base_wpath=None):
        self.base_rpath = base_rpath
        self.base_wpath = base_wpath

    def read(self, relative_path=None):
        target_path = self.base_rpath
        if relative_path is not None:
            target_path = os.path.join(self.base_rpath, relative_path)

        messages = []
        for f in os.listdir(target_path):
            f_path = os.path.join(target_path, f)
            if not os.access(f_path, os.F_OK|os.R_OK):
                logger.error('cache read file with exception, mode=F_OK|R_OK path={0}'.format(f_path))
                continue
            if not os.path.isfile(f_path):
                continue
            content = File.read_content(f_path)
            messages.append(content)

        return messages

    def write(self, content, relative_path=None):
        target_path = self.base_rpath
        if relative_path is not None:
            target_path = os.path.join(self.base_rpath, relative_path)
        if os.path.exists(target_path):
            logger.warning('cache file has not been consumed, ignore, path={0}'.format(target_path))
            return
        File.write_content(content, target_path)
