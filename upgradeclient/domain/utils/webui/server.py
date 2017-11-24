#! -*- coding: utf-8 -*-

import os
import web


from upgradeclient.domain.utils.webui.views import *
from upgradeclient.domain.utils.webui.config import template_dir
from upgradeclient.domain.utils.webui.urls import url_patterns as urls
from upgradeclient.domain.utils.webui.middleware import LogMiddleware, ExpMiddleware


app = web.application(urls, globals())
render = web.template.render('{0}/'.format(template_dir), cache=False)

# 自定义404/500页面
app.notfound = lambda e: web.notfound(render.error(content=e))
app.internalerror = lambda e: web.internalerror(render.error(content=e))


def run(*middleware, **envs):
    map(lambda k: os.environ.setdefault(k.upper(), str(envs[k])), envs)
    app.run(LogMiddleware, ExpMiddleware, *middleware)
