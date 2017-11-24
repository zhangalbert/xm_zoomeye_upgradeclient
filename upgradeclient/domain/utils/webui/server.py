#! -*- coding: utf-8 -*-

import os
import web


from upgradeclient.domain.utils.webui.views import *
from upgradeclient.domain.utils.webui.config import template_dir
from upgradeclient.domain.utils.webui.middleware import LogMiddleware
from upgradeclient.domain.utils.webui.urls import url_patterns as urls


app = web.application(urls, globals())
render = web.template.render('{0}/'.format(template_dir), base=os.path.join(template_dir, 'ebase.html'), cache=False)

# 自定义404/500页面
app.notfound = lambda: web.notfound(render.error())
app.internalerror = lambda: web.internalerror(render.error())


def run(*middleware, **envs):
    map(lambda k: os.environ.setdefault(k.upper(), str(envs[k])), envs)
    app.run(LogMiddleware, *middleware)
