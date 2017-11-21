#! -*- coding: utf-8 -*-


import os
import datetime


from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.utils.download import Download
from upgradeclient.domain.utils.firmware import Firmware
from upgradeclient.domain.bl.handlers.base import BaseHandler
from upgradeclient.domain.model.event.event_type import EventType
from upgradeclient.domain.bl.event.event_handler import EventHandler


logger = Logger.get_logger(__name__)


class ReleaseNoteHandler(BaseHandler):
    def send_task_cache(self, obj):
        pass

    def create_event(self, obj, **kwargs):
        event = EventHandler.create_event(event_name=EventType.DOWNLOADING_FIRMWARE, **kwargs)
        event.set_daoname(obj.get_daoname())
        event.set_filetype(obj.get_filetype())
        event.set_author(obj.get_author())

        return event

    def generate_url(self, obj, data, ):
        pass

    def analysis_log(self, obj):
        fdirname = os.path.join(self.cache.base_path, 'download_cache')
        filename = os.path.join(fdirname, obj.get_filename())
        dict_data = Firmware.release_note2dict(filename)
        if not dict_data:
            logger.warning('resolve release_note with exception, path={0}'.format(filename))
        ins = self.dao_factory[obj.get_daoname()]
        end_time = datetime.datetime.now()
        sta_time = end_time - datetime.timedelta(seconds=ins.revision_seconds)
        for key, val in dict_data:
            date, flag = key
            if date < sta_time.strftime('%Y-%m-%d'):
                continue
            event = self.create_event(obj)

    def handle(self, obj):
        """ 处理DOWNLOADING_RELEASENOTE事件
        1. 下载release_note文件到download_cache
        2. 下载成功调用analysis_log解析release_note文件
        3. 结束后删除check_cache内对应的任务
        """
        fdirname = os.path.join(self.cache.base_path, 'download_cache')
        filename = os.path.join(fdirname, obj.get_filename())

        download = Download()
        download.reg_reporthook()
        dwresult = download.wget(obj.get_download_url(), filename)

        if not dwresult:
            return

        # self.analysis_log(obj)

        fdirname = os.path.join(self.cache.base_path, 'check_cache')
        filename = os.path.join(fdirname, obj.get_filename())
        if os.path.exists(filename):
            os.remove(filename)


