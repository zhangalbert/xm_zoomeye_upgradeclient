#! -*- coding: utf-8 -*-

import os
import time
import datetime
import multiprocessing


from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.model.event.event import Event
from upgradeclient.service.base_service import BaseService
from upgradeclient.domain.model.event.event_type import EventType


logger = Logger.get_logger(__name__)


class CheckHandlerProcess(multiprocessing.Process):
    def __init__(self, obj, service):
        super(CheckHandlerProcess, self).__init__()
        self.obj = obj
        self.service = service

    def run(self):
        ins = self.obj.get_data()
        self.service.handle(ins)


class CheckService(BaseService):
    def __init__(self, check=None, cache=None, dao_factory=None, filter_factory=None):
        self.check = check
        self.cache = cache
        self.sub_process = {}
        self.dao_factory = dao_factory
        self.filter_factory = filter_factory

    def pre_start(self):
        fdirname = os.path.join(self.cache.base_path, 'check_cache')
        not os.path.exists(fdirname) and os.makedirs(fdirname)

    def post_start(self):
        pass

    def start(self):
        self.pre_start()
        for name in self.dao_factory.check_daos:
            dao = self.dao_factory.create_check_dao(name)
            p = CheckHandlerProcess(dao, self)
            p.daemon = True
            p.start()
            self.sub_process[name] = p
        for name in self.sub_process:
            self.sub_process[name].join()

    def send_cache_task(self, event):
        json_data = event.to_json()
        relative_path = os.path.join('check_cache', event.get_filename())
        self.cache.write(json_data, relative_path=relative_path)

    def create_event(self, **kwargs):
        event = Event(name=EventType.downloading_releasenote, **kwargs)

        return event

    def get_baseurl(self, url):
        parent_url = os.path.dirname(url)
        base_url = os.path.dirname(parent_url)

        return base_url

    def get_filter_handler(self, obj):
        filter_handler_name = obj.get_name()
        filter_handler = self.filter_factory.create_filter_handler(filter_handler_name)

        return filter_handler

    def get_latest_changes(self, obj):
        latest_changes = []
        split_latest_changes = {'releasenotes': [], 'firmwares': []}

        url, name, summarize_interval = obj.get_base_url(), obj.get_name(), obj.get_summarize_interval()
        end_time = datetime.datetime.now() + datetime.timedelta(days=1)
        sta_time = datetime.datetime.now() - datetime.timedelta(days=1, seconds=obj.get_revision_seconds())
        try:
            latest_changes = self.check.revision_summarize(url, sta_time.timetuple(), end_time.timetuple())
        except Exception as e:
            fmtdata = (self.__class__.__name__, name, summarize_interval, os.getpid(), e)
            msgdata = '{0} sub process {1} check with exception, wait {2} seconds, pid={3} exp={4}'.format(*fmtdata)
            self.insert_to_db(log_level='error', log_message=msgdata)
            logger.error(msgdata)

        filter_handler = self.get_filter_handler(obj)
        for item in latest_changes:
            cobj = type('cobj', (object,), item)
            if not filter_handler.release_note_validate(cobj):
                split_latest_changes['firmwares'].append(cobj)
                continue
            split_latest_changes['releasenotes'].append(cobj)

        return split_latest_changes

    def handle(self, obj):
        url, name, summarize_interval = obj.get_base_url(), obj.get_name(), obj.get_summarize_interval()

        self.check.set_commit_info_style(style_num=1)

        while True:
            latest_changes = self.get_latest_changes(obj)
            
            if not latest_changes:
                fmtdata = (self.__class__.__name__, summarize_interval)
                logger.warning('{0} check with not latest changes, wait {1} seconds'.format(*fmtdata))
                time.sleep(summarize_interval)
                continue

            merged_changes = {}
            merged_urlmaps = {}
            filter_handler = self.get_filter_handler(obj)
            split_latest_changes = self.get_latest_changes(obj)
            for robj in split_latest_changes['releasenotes']:
                base_url = os.path.dirname(robj.download_url)
                merged_urlmaps.setdefault(base_url, robj)
                merged_changes.setdefault(base_url, [])
                for cobj in split_latest_changes['firmwares']:
                    if base_url in cobj.download_url and filter_handler.firmware_name_validate(cobj):
                        merged_changes[base_url].append(cobj)

            for item in merged_urlmaps:
                event_data = map(lambda e: self.create_event(daoname=obj.get_name(), **dict(e.__dict__)).to_json(),
                                 merged_changes[item])
                event = self.create_event(daoname=obj.get_name(), **dict(merged_urlmaps[item].__dict__))
                event.set_data(event_data)

                self.send_cache_task(event)

            time.sleep(summarize_interval)

