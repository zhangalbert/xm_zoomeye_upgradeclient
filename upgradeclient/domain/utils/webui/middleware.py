#! -*- coding: utf-8 -*-


import web
import traceback


from wsgilog import WsgiLog
from upgradeclient.domain.utils.webui.config import template_dir, env


HTTPMSG = '500 Internal Error'
ERRORMSG = 'Server got itself in trouble'


render = web.template.render('{0}/'.format(template_dir), cache=False)


class ExpMiddleware(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(self, application, errapp=self._errapp, **env)

    def _errapp(self, environ, start_response):
        html = render.error(content=traceback.format_exc())
        start_response(HTTPMSG, [('Content-type', 'text/plain')], html)
        return [ERRORMSG]


