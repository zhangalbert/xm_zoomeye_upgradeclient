#! -*- coding: utf-8 -*-


import time
import multiprocessing


from threading import Thread
from concurrent import futures
from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class UploadService(object):
    def __init__(self, cache=None, check_interval=None, dao_factory=None, upload_factory=None):
        self.cache = cache
        self.dao_factory = dao_factory
        self.check_interval = check_interval
        self.upload_factory = upload_factory

    def start(self):
        """ 启动upload_service

        """
        def target():
            while True:
                future_to_ins = {}
                for name in self.dao_factory:
                    uhandler = self.upload_factory[name]
                    ins_list = self.dao_factory[name].get_data()
                    max_workers = min(len(ins_list), multiprocessing.cpu_count())
                    with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                        future_to_ins = dict(map(lambda ins: (executor.submit(uhandler.handle, ins)), ins_list))

                for future in futures.as_completed(future_to_ins):
                    ins = future_to_ins[future]
                    if future.exception() is not None:
                        fmtdata = (ins.get_remoteurl(), future.exception())
                        logger.error('upload to {0} with exception, exp={1}'.format(*fmtdata))
                    else:
                        logger.info('upload to {0} successfully'.format(ins.get_remoteurl()))

                time.sleep(self.check_interval)

        t = Thread(target=target)
        t.setDaemon(True)
        t.start()
