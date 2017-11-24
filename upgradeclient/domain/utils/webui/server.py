#! -*- coding: utf-8 -*-


import web


from upgradeclient.domain.utils.webui.views import *
from upgradeclient.domain.utils.webui.config import template_dir
from upgradeclient.domain.utils.webui.urls import url_patterns as urls
from upgradeclient.domain.utils.webui.middleware import LogMiddleware


app = web.application(urls, globals())
render = web.template.render('{0}/'.format(template_dir), cache=False)
# 自定义404/500异常
app.notfound = lambda: web.notfound(render.error(content='not found'))
app.internalerror = lambda: web.internalerror(render.error(content='internal error'))


def run(*middleware, **envs):
    map(lambda k: os.environ.setdefault(k.upper(), str(envs[k])), envs)
    app.run(LogMiddleware, *middleware)
