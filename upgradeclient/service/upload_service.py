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
    def __init__(self, cache=None, check_interval=None, dao_factory=None, handler_factory=None):
        self.cache = cache
        self.dao_factory = dao_factory
        self.check_interval = check_interval
        self.handler_factory = handler_factory

    def pre_start(self):
        fdirname = os.path.join(self.cache.base_path, 'upgrade_files')
        not os.path.exists(fdirname) and os.makedirs(fdirname)

    def post_start(self):
        pass

    def merge_task(self):
        fdirname = os.path.join(self.cache.base_path, 'upgrade_files')

        handler_dao_map = []
        for name in self.dao_factory.check_daos:
            conf_dao = self.dao_factory.create_check_dao(name)
            dao_data = conf_dao.get_data()
            dir_path = os.path.join(fdirname, dao_data.get_target_cache())
            not os.path.exists(dir_path) and os.makedirs(dir_path)

            upload_list = dao_data.get_upload()
            for u in upload_list:
                u_type = u.get_relation_type()
                u_handler = self.handler_factory.create_upload_handler(u_type)
                handler_dao_map.append((u_handler, u))

        return handler_dao_map

    def start(self):
        self.pre_start()

        def target():
            while True:
                future_to_ins = {}
                handler_dao_map = self.merge_task()
                max_workers = min(len(handler_dao_map), multiprocessing.cpu_count())

                with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future_to_ins = dict(map(lambda o: (executor.submit(o[0].handle, o[1]), o[1]), handler_dao_map))

                for future in futures.as_completed(future_to_ins):
                    ins = future_to_ins[future]

                    relation_name = ins.get_relation_name()
                    relation_type = ins.get_relation_type()
                    exception = future.exception()
                    if future.exception() is not None:
                        fmtdata = (self.__class__.__name__, relation_name, relation_type, exception)
                        msgdata = '{0} upload with {1}/{2} exception, exp={3}'.format(*fmtdata)
                        self.insert_to_db(log_level='error', log_message=msgdata)
                        logger.error(msgdata)
                    else:
                        fmtdata = (self.__class__.__name__, relation_name, relation_type, exception)
                        msgdata = '{0} upload with {1}/{2} success'.format(*fmtdata)
                        logger.info(msgdata)

                time.sleep(self.check_interval)

        t = Thread(target=target)
        t.setDaemon(True)
        t.start()
