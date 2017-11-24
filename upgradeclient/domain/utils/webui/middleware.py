#! -*- coding: utf-8 -*-


import web
import traceback


from wsgilog import WsgiLog
from upgradeclient.domain.utils.webui.config import template_dir, env


CATCHID = 'wsgilog.catch'
LOGGERID = 'wsgilog.logger'
THROWERR = 'x-wsgiorg.throw_errors'


render = web.template.render('{0}/'.format(template_dir), cache=False)


class ExpMiddleware(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        try:
            response = self.application(environ, start_response)

            rsp_errs = environ['wsgi.errors'].read()
            if rsp_errs.strip():
                return response
            return render.error(content=rsp_errs)
        except:
            return render.error(content=traceback.format_exc())


class LogMiddleware(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(self, application, **env)




