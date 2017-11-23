#! -*- coding: utf-8 -*-


from threading import Thread
from upgradeclient.domain.utils.webui import server


class WebuiService(object):
    def __init__(self, *middleware, **envs):
        self.middleware = middleware
        self.envs = envs or {'port': 80}

    def start(self, ):
        t = Thread(server.run, args=self.middleware, kwargs=self.envs)
        t.setDaemon(True)
        t.start()
