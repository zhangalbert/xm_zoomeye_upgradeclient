#! -*- coding: utf-8 -*-


import os
import json
import datetime


from upgradeclient.domain.common.filter import Q, R
from upgradeclient.domain.utils.extstr import ExtStr
from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.utils.download import Download
from upgradeclient.domain.utils.firmware import Firmware
from upgradeclient.domain.model.event.event import Event
from upgradeclient.domain.model.event.event_type import EventType
from upgradeclient.domain.bl.handlers.download.base import BaseHandler


logger = Logger.get_logger(__name__)


class ReleaseNoteHandler(BaseHandler):
    def send_task_cache(self, event):
        json_data = event.to_json()
        relative_path = os.path.join('check_cache', event.get_filename())
        self.cache.write(json_data, relative_path=relative_path)

    def create_event(self, **kwargs):
        kwargs.pop('name')
        event = Event(name=EventType.DOWNLOADING_FIRMWARE, **kwargs)

        return event

    def filter_event(self, q, objs_list):
        event_list = []
        for obj in objs_list:
            obj.filename = ExtStr(obj.filename)
            obj.download_url = ExtStr(obj.download_url)
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

        conf_dao = self.dao_factory[obj.get_daoname()]
        ins = conf_dao.get_data()
        end_time = datetime.datetime.now()
        sta_time = end_time - datetime.timedelta(seconds=ins.revision_seconds)

        for key, val in dict_data.iteritems():
            date, flag = key
            sta_date = sta_time.strftime('%Y-%m-%d')
            end_date = end_time.strftime('%Y-%m-%d')
            if date < sta_date or date > end_date:
                logger.debug('{0} delected invalid date-range, cur_date={1} sta_date={2} end_date={3}, url={4}'.format(
                    self.__class__.__name__, date, sta_date, end_date, obj.get_download_url()
                ))
                continue
            q = Q(obj__download_url__contains=date) & Q(obj__filename__contains=flag)
            filter_res = self.filter_event(q, objs_list)
            filter_res and val.update({'Date': date})
            map(lambda e: e.set_data(val), filter_res)
            event_list.extend(filter_res)

        return event_list

    def handle(self, obj):
        """ 处理DOWNLOADING_RELEASENOTE事件
        1. 下载release_note文件到download_cache
        2. 下载成功调用analysis_log解析release_note文件
        3. 结束后删除check_cache内对应的任务
        """
        tdirname = os.path.join(self.cache.base_path, 'download_cache')
        sdirname = os.path.join(self.cache.base_path, 'check_cache')
        dst_name = os.path.join(tdirname, obj.get_filename())
        src_name = os.path.join(sdirname, obj.get_filename())

        download = Download()
        if not download.wget(obj.get_download_url(), dst_name):
            return
        event_list = self.analysis_log(obj)
        for event in event_list:
            self.send_task_cache(event)
        self.delete(src_name, dst_name)





