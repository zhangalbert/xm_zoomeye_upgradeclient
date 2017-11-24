#! -*- coding: utf-8 -*-


import os
import web


from wsgilog import WsgiLog
from upgradeclient.domain.utils.webui.config import template_dir, env


CATCHID = 'wsgilog.catch'
LOGGERID = 'wsgilog.logger'
THROWERR = 'x-wsgiorg.throw_errors'


class LogMiddleware(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(self, application, **env)

    def __call__(self, environ, start_response):
        if self.log:
            environ[LOGGERID] = self.logger
        environ[CATCHID] = self.catch
        if THROWERR in environ:
            return self.application(environ, start_response)
        try:
            return self.application(environ, start_response)
        except:
            content = self.catch(environ, start_response)
            render = web.template.render('{0}/'.format(template_dir), base=os.path.join(template_dir, 'ebase'),
                                         globals={'content': content}, cache=False)
            return render.error()

