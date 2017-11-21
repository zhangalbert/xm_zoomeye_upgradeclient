#! -*- coding: utf-8 -*-


import os
import json
import datetime


from upgradeclient.domain.common.filter import Q, R
from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.utils.download import Download
from upgradeclient.domain.utils.firmware import Firmware
from upgradeclient.domain.bl.handlers.base import BaseHandler
from upgradeclient.domain.model.event.event_type import EventType
from upgradeclient.domain.bl.event.event_handler import EventHandler


logger = Logger.get_logger(__name__)


class ReleaseNoteHandler(BaseHandler):
    def send_task_cache(self, event):
        json_data = event.to_json()
        relative_path = os.path.join('check_cache', event.get_filename())
        self.cache.write(json_data, relative_path=relative_path)

    def create_event(self, **kwargs):
        event = EventHandler.create_event(event_name=EventType.DOWNLOADING_FIRMWARE, **kwargs)

        return event

    def filter_event(self, q, objs_list):
        event_list = []
        for obj in objs_list:
            res = R(obj, q_ins=q)()
            if res is True:
                event = self.create_event(**dict(obj.__dict__))
                event_list.append(event)
        return event_list

    def analysis_log(self, obj):
        event_list = []
        fdirname = os.path.join(self.cache.base_path, 'download_cache')
        filename = os.path.join(fdirname, obj.get_filename())
        if not obj.get_data():
            logger.warning('release_not with no firmwares list data, url={0}'.format(obj.get_download_url()))
            return event_list
        objs_list = map(lambda o: type('obj', (object,), json.loads(o)), obj.get_data())

        dict_data = Firmware.release_note2dict(filename)
        if not dict_data:
            logger.warning('resolve release_note with exception, url={0} path={1}'.format(obj.get_download_url(),
                                                                                          filename))
            return event_list

        ins = self.dao_factory[obj.get_daoname()]
        end_time = datetime.datetime.now()
        sta_time = end_time - datetime.timedelta(seconds=ins.revision_seconds)
        for key, val in dict_data:
            date, flag = key
            if date < sta_time.strftime('%Y-%m-%d') or date > end_time.strftime('%Y-%m-%d'):
                logger.debug('{0} delected invalid date-range, ignore, url={0}'.format(obj.get_download_url()))
                continue
            q = Q(obj__download_url__contains=date) & Q(obj__filename__contains=flag)
            event_list.extend(self.filter_event(q, objs_list))

        return event_list

    def cleaning(self, **args):
        for f in args:
            if not os.path.exists(f):
                continue
            os.remove(f)

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
        download.wget(obj.get_download_url(), filename)

        event_list = self.analysis_log(obj)
        for event in event_list:
            self.send_task_cache(event)

        fdirname = os.path.join(self.cache.base_path, 'check_cache')
        filename = os.path.join(fdirname, obj.get_filename())
        self.cleaning(filename)
