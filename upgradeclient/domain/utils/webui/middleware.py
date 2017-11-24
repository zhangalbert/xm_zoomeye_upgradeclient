#! -*- coding: utf-8 -*-


from wsgilog import WsgiLog
from upgradeclient.domain.utils.webui.config import env


class LogMiddleware(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(self, application, **env)
