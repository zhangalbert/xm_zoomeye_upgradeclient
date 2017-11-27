#! -*- coding: utf-8 -*-


import os
import time


from threading import Thread
from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.model.event.event import Event
from upgradeclient.service.base_service import BaseService


logger = Logger.get_logger(__name__)


class DownloadHandlerThread(Thread):
    def __init__(self, json_data, service):
        super(DownloadHandlerThread, self).__init__()
        self.service = service
        self.json_data = json_data

    def run(self):
        event = Event.from_json(self.json_data)
        self.service.handle(event)


class DownloadService(BaseService):
    def __init__(self, cache=None, handler_factory=None, abstruct_path=None, relative_path=None, check_interval=15):
        self.cache = cache
        self.sub_threads = []
        self.abstruct_path = abstruct_path
        self.relative_path = relative_path
        self.handler_factory = handler_factory
        self.check_interval = check_interval or 15

    def start(self):
        """ 启动download_service

        """
        # 防止线程之间竞争makedirs导致OSError
        fdirname = os.path.join(self.cache.base_path, 'download_cache')
        not os.path.exists(fdirname) and os.makedirs(fdirname)

        def target():
            while True:
                messages = self.cache.read(self.abstruct_path, self.relative_path)
                if not messages:
                    time.sleep(self.check_interval)
                    continue
                for message in messages:
                    t = DownloadHandlerThread(message, self)
                    t.setDaemon(True)
                    t.start()
                    self.sub_threads.append(t)

                while True:
                    threads_status = map(lambda _: not _.isAlive(), self.sub_threads)
                    if all(threads_status):
                        break
                    time.sleep(1)
                fmtdata = (self.__class__.__name__, self.check_interval, len(messages))
                msgdata = '{0} thread group is finished, wait {1} seconds, num={2}'.format(*fmtdata)
                self.insert()(log_level='info', log_message=msgdata)
                logger.info(msgdata)
                time.sleep(self.check_interval)
        t = Thread(target=target)
        t.setDaemon(True)
        t.start()

    def handle(self, obj):
        fdirname = os.path.join(self.cache.base_path, 'download_cache')
        filepath = os.path.join(fdirname, obj.get_filename())
        if os.path.exists(filepath):
            fmtdata = (self.__class__.__name__, filepath)
            msgdata = '{0} download_cache file has not been consumed, ignore, path={0}'.format(*fmtdata)
            # self.insert()(log_level='warning', log_message=msgdata)
            logger.warning(msgdata)
            return
        handler = self.handler_factory.create_download_handler(obj)
        handler.handle(obj)
