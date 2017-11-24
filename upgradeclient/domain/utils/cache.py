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
            fmtdata = (self.__class__.__name__, relative_path, target_path)
            msgdata = '{0} detected {1} cache dir is not ready, path={2}'.format(*fmtdata)
            logger.warning(msgdata)
            return messages

        for f in os.listdir(target_path):
            f_path = os.path.join(target_path, f)
            if not os.access(f_path, os.F_OK|os.R_OK):
                fmtdata = (self.__class__.__name__, relative_path, f_path)
                msgdata = '{0} read {1} cache with exception, mode=F_OK|R_OK path={2}'.format(*fmtdata)
                logger.error(msgdata)
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
            fmtdata = (self.__class__.__name__, relative_path, target_path)
            msgdata = '{0} detected {1} cache with same file, wait consumed, path={2}'.format(fmtdata)
            logger.warning(msgdata)
            return
        File.write_content(content, target_path)
