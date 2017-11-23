#! -*- coding: utf-8 -*-

import os
import web


from upgradeclient.domain.utils.webui.views import *
from upgradeclient.domain.utils.webui.urls import url_patterns as urls


app = web.application(urls, globals())


def run(*middleware, **envs):
    map(lambda k: os.environ.setdefault(k.upper(), str(envs[k])), envs)
    app.run(*middleware)
