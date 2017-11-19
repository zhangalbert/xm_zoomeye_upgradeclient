#! -*- coding: utf-8 -*-


import time
import signal


from multiprocessing import Process


class CheckHandlerProcess(Process):
    def __init__(self, name, obj, service):
        super(CheckHandlerProcess, self).__init__()
        self.obj = obj
        self.name = name
        self.service = service

    def run(self):
        ins = self.obj.get_data()
        self.service.handle(self.name, ins)


class CheckService(object):
    def __init__(self, check=None, cache=None, dao_factory=None, filter_factory=None):
        self.check = check
        self.cache = cache
        self.sub_process = {}
        self.dao_factory = dao_factory
        self.filter_factory = filter_factory

    def signal_callback(self, signal_num, unused_frame):
        if signal_num in (signal.SIGINT, signal.SIGTERM):
            self.stop()
            return
        for name in self.sub_process:
            p = self.sub_process[name]
            if not p.is_alive():
                sub_p = CheckHandlerProcess(name, self.dao_factory[name], self)
                sub_p.daemon = True
                sub_p.start()
                self.sub_process.pop(name)
                self.sub_process.update({name: sub_p})

    def stop(self):
        if not self.sub_process:
            return
        for name in self.sub_process:
            p = self.sub_process[name]
            if p.is_alive():
                p.terminate()

    def start(self):
        """ 启动check_service

        1. 多进程同时检测多个base_url是否有更新
        2. 子进程挂掉后自动重启
        3. 回调将任务写入cacher
        """
        for name in self.dao_factory:
            p = CheckHandlerProcess(name, self.dao_factory[name], self)
            p.daemon = True
            p.start()
            self.sub_process.update({name: p})
        signal.signal(signal.SIGCHLD, self.signal_callback)
        while True:
            signal.pause()

    def send_cache_task(self, obj):
        print '='*50
        print obj.filename, obj.download_url
        print '='*50

    def handle(self, name, ins):
        url = ins.get_base_url()
        filter_ins = self.filter_factory[name]
        self.check.set_commit_info_style(style_num=1)
        while True:
            end_timestamp = time.time()
            start_timestamp = end_timestamp - ins.revision_seconds
            latest_changes = self.check.revision_summarize(url, start_timestamp, end_timestamp)
            for item in latest_changes:
                obj = type('obj', (object,), item)
                res = filter_ins.release_note_validate(obj)
                if not res:
                    continue
                self.send_cache_task(obj)

            time.sleep(ins.summarize_interval)