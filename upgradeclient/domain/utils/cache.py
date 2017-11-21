#! -*- coding: utf-8 -*-


import os


from upgradeclient.domain.common.file import File
from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class Cache(object):
    def __init__(self, base_path=None):
        self.base_path = base_path

    def read(self, abstruct_path=None, relative_path=None):
        messages = []
        target_path = abstruct_path or self.base_path
        if relative_path is not None:
            target_path = os.path.join(target_path, relative_path)
        if not os.path.exists(target_path):
            logger.warning('cache dir is not ready, path={0}'.format(target_path))
            return messages

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

    def write(self, content, abstruct_path=None, relative_path=None):
        target_path = abstruct_path or self.base_path
        if relative_path is not None:
            target_path = os.path.join(target_path, relative_path)
        if os.path.exists(target_path):
            logger.warning('cache file has not been consumed, ignore, path={0}'.format(target_path))
            return
        File.write_content(content, target_path)
