#! -*- coding: utf-8 -*-

import os
import time
import signal
import datetime
import multiprocessing


from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.model.event.event import Event
from upgradeclient.service.base_service import BaseService
from upgradeclient.domain.model.event.event_type import EventType


logger = Logger.get_logger(__name__)


class CheckHandlerProcess(multiprocessing.Process):
    def __init__(self, name, obj, service):
        super(CheckHandlerProcess, self).__init__()
        self.obj = obj
        self.name = name
        self.service = service

    def run(self):
        ins = self.obj.get_data()
        self.service.handle(self.name, ins)


class CheckService(BaseService):
    def __init__(self, check=None, cache=None, dao_factory=None, filter_factory=None):
        self.check = check
        self.cache = cache
        self.sub_process = {}
        self.event_event = multiprocessing.Event()
        self.dao_factory = dao_factory
        self.filter_factory = filter_factory

    def sub_process_signal_callback(self, signal_num, unused_frame):
        if self.event_event.is_set():
            return
        for name in self.sub_process:
            p = self.sub_process[name]
            if not p.is_alive():
                sub_p = CheckHandlerProcess(name, self.dao_factory[name], self)
                sub_p.daemon = True
                sub_p.start()
                self.sub_process.pop(name)
                self.sub_process.update({name: sub_p})

    def ctl_process_signal_callback(self, unused_signal, unused_frame):
        fmtdata = (self.__class__.__name__, multiprocessing.current_process(), os.getpid())
        msgdata = '{0} main/sub process got ctrl+c signal, name={1}, pid={2}'.format(*fmtdata)
        self.insert()(log_level='warning ',  log_message=msgdata)
        logger.warning(msgdata)

    def start(self):
        """ 启动check_service

        1. 多进程同时检测多个base_url是否有固件更新
        2. 子进程异常后自动启动同配置子进程
        3. 多进程检测数据通过对应子类过滤器最终生成下载任务对象
        4. 异步回调写入下载任务对象到本地cacher
        5. 优雅关闭,等待所有子进程任务执行完后,主进程关闭
        """
        # 防止进程之间竞争makedirs导致OSError
        fdirname = os.path.join(self.cache.base_path, 'check_cache')
        not os.path.exists(fdirname) and os.makedirs(fdirname)

        for name in self.dao_factory:
            p = CheckHandlerProcess(name, self.dao_factory[name], self)
            p.daemon = True
            p.start()
            self.sub_process.update({name: p})
        signal.signal(signal.SIGCHLD, self.sub_process_signal_callback)
        signal.signal(signal.SIGINT,  self.ctl_process_signal_callback)
        while True:
            is_finished = True
            for name in self.sub_process:
                p = self.sub_process[name]
                if p.is_alive():
                    is_finished = False
                    break
            if is_finished is True:
                break
            time.sleep(15)
        fmtdata = (self.__class__.__name__,)
        msgdata = '{0} graceful closing successfully!'.format(*fmtdata)
        self.insert()(log_level='info', log_message=msgdata)
        logger.info(msgdata)

    def send_cache_task(self, event):
        json_data = event.to_json()
        relative_path = os.path.join('check_cache', event.get_filename())
        self.cache.write(json_data, relative_path=relative_path)

    def create_event(self, **kwargs):
        event = Event(name=EventType.DOWNLOADING_RELEASENOTE, **kwargs)

        return event

    def get_baseurl(self, url):
        parent_url = os.path.dirname(url)
        base_url = os.path.dirname(parent_url)

        return base_url

    def handle(self, name, ins):
        url = ins.get_base_url()
        filter_ins = self.filter_factory[name]
        self.check.set_commit_info_style(style_num=1)
        signal.signal(signal.SIGINT, self.ctl_process_signal_callback)

        while True:
            if self.event_event.is_set():
                fmtdata = (self.__class__.__name__, name, os.getpid())
                msgdata = '{0} sub process {1} stoped successfull, pid={1}'.format(*fmtdata)
                self.insert()(log_level='info', log_message=msgdata)
                logger.info(msgdata)
                break
            end_time = datetime.datetime.now()
            sta_time = end_time - datetime.timedelta(seconds=ins.revision_seconds)
            try:
                latest_changes = self.check.revision_summarize(url, sta_time.timetuple(),
                                                               end_time.timetuple())
            except Exception as e:
                fmtdata = (self.__class__.__name__, name, ins.summarize_interval, os.getpid(), e)
                msgdata = '{0} sub process {1} check with exception, wait {2} seconds, pid={3} exp={4}'.format(*fmtdata)
                self.insert()(log_level='error', log_message=msgdata)
                logger.error(msgdata)
                time.sleep(ins.summarize_interval)
                continue
            merged_changes = {}
            merged_urlmaps = {}
            for item in latest_changes:
                obj = type('obj', (object,), item)
                base_url = self.get_baseurl(obj.download_url)
                if not filter_ins.release_note_validate(obj):
                    if base_url in merged_changes and filter_ins.firmware_name_validate(obj):
                        merged_changes[base_url].append(obj)
                    continue
                merged_changes.setdefault(os.path.dirname(obj.download_url), [])
                merged_urlmaps.setdefault(os.path.dirname(obj.download_url), obj)

            for item in merged_urlmaps:
                event = self.create_event(daoname=name, **dict(merged_urlmaps[item].__dict__))
                event_data = map(lambda e: self.create_event(daoname=name, **dict(e.__dict__)).to_json(),
                                 merged_changes[item])
                event.set_data(event_data)
                self.send_cache_task(event)

            time.sleep(ins.summarize_interval)
