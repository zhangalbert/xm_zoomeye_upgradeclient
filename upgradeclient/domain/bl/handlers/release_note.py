#! -*- coding: utf-8 -*-


import os


from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.utils.download import Download
from upgradeclient.domain.bl.handlers.base import BaseHandler


logger = Logger.get_logger(__name__)


class ReleaseNoteHandler(BaseHandler):
    def handle(self, obj):
        """

        1. 下载指定文件到download_cache目录
        2. 如果下载成功并处理完毕后再删除原check_cache文件
        """
        fdirname = os.path.join(self.cache.base_path, 'download_cache')
        filename = os.path.join(fdirname, obj.get_filename())

        download = Download()
        # 使用默认回调
        download.reg_reporthook()
        dwresult = download.wget(obj.get_download_url(), filename)

        fdirname = os.path.join(self.cache.base_path, 'check_cache')
        filename = os.path.join(fdirname, obj.get_filename())

        if dwresult:
            os.remove(filename)


