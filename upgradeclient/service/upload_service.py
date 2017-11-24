#! -*- coding: utf-8 -*-


import os
import time
import multiprocessing


from threading import Thread
from concurrent import futures
from upgradeclient.domain.common.logger import Logger
from upgradeclient.service.base_service import BaseService


logger = Logger.get_logger(__name__)


class UploadService(BaseService):
    def __init__(self, cache=None, check_interval=None, dao_factory=None, upload_factory=None):
        self.cache = cache
        self.dao_factory = dao_factory
        self.check_interval = check_interval
        self.upload_factory = upload_factory

    def start(self):
        """ 启动upload_service

        """
        # 防止线程之间竞争makedirs导致OSError
        fdirname = os.path.join(self.cache.base_path, 'upgrade_files')
        not os.path.exists(fdirname) and os.makedirs(fdirname)

        def target():
            while True:
                future_to_ins = {}
                for name in self.dao_factory:
                    uhandler = self.upload_factory[name]
                    ins_list = self.dao_factory[name].get_data()
                    max_workers = min(len(ins_list), multiprocessing.cpu_count())
                    with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                        future_to_ins = dict(map(lambda o: (executor.submit(uhandler.handle, o), o), ins_list))

                for future in futures.as_completed(future_to_ins):
                    ins = future_to_ins[future]
                    if future.exception() is not None:
                        fmtdata = (self.__class__.__name__, ins.get_remoteurl(), future.exception())
                        msgdata = '{0} upload with {1} with exception, exp={2}'.format(*fmtdata)
                        self.insert()(log_level='error', log_message=msgdata)
                        logger.error(msgdata)
                    else:
                        fmtdata = (self.__class__.__name__, ins.get_remoteurl(), future.exception())
                        msgdata = '{0} upload with {1} success'.format(*fmtdata)
                        logger.info(msgdata)
                time.sleep(self.check_interval)

        t = Thread(target=target)
        t.setDaemon(True)
        t.start()
