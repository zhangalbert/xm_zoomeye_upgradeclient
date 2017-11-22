#! -*- coding: utf-8 -*-


import os


from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.utils.download import Download
from upgradeclient.domain.bl.handlers.base import BaseHandler


logger = Logger.get_logger(__name__)


class FirmwareHandler(BaseHandler):
    def analysis_log(self, obj):
        task_list = []
        fdirname = os.path.join(self.cache.base_path, 'download_cache')
        fsrcname = obj.get_filename().rsplit('_', 1)[0]
        filename = os.path.join(fdirname, fsrcname)

        eventdata = obj.get_data()

        return task_list

    def handle(self, obj):
        """ 处理DOWNLOADING_FIRMWARE事件
        1. 下载.bin文件到download_cache
        2. 下载成功调用analysis_log解析event_data数据并创建指定升级目录
        3. 结束后删除check_cache内对应的任务
        """
        sdirname = os.path.join(self.cache.base_path, 'check_cache')
        tdirname = os.path.join(self.cache.base_path, 'download_cache')
        fsrcname = obj.get_filename().rsplit('_', 1)[0]
        src_name = os.path.join(sdirname, obj.get_filename())
        dst_name = os.path.join(tdirname, fsrcname)

        download = Download()
        if not download.wget(obj.get_download_url(), dst_name):
            return
        task_list = self.analysis_log(obj)

        # self.delete(src_name)




