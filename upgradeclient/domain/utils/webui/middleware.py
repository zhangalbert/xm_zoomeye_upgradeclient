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
            res = self.application(environ, start_response)
            print 'limanman'
            for x in res:
                print x
            return res
        except:
            return render.error(content=self.catch(environ, start_response))

    def catch(self, environ, start_response):
        return traceback.format_exc()


class LogMiddleware(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(self, application, **env)




