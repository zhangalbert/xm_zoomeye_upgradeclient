#! -*- coding: utf-8 -*-


import web
import sys


from wsgilog import WsgiLog
from upgradeclient.domain.utils.webui.config import template_dir, env


render = web.template.render('{0}/'.format(template_dir), cache=False)


class ExpMiddleware(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(self, application, **env)
        self.catch = self.__catch

    def __catch(self, environ, start_response):
        if self.log:
            self.logger.exception(self.message)
        if self.debug:
            return render.error(content=sys.exc_info())




