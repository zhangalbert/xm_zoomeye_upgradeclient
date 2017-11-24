#! -*- coding: utf-8 -*-

import os
import web
import traceback


from upgradeclient.domain.utils.webui.config import template_dir


exp_render = web.template.render('{0}/'.format(template_dir), cache=False)
com_render = web.template.render('{0}/'.format(template_dir), base=os.path.join(template_dir, 'layout'), cache=False)


class BaseView(object):
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def post(self, *args, **kwargs):
        raise NotImplementedError

    def GET(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except:
            return exp_render.error(content=traceback.format_exc())

    def POST(self, *args, **kwargs):
        try:
            return self.post(*args, **kwargs)
        except:
            return exp_render.error(content=traceback.format_exc())


class RedirectView(BaseView):
    def get(self, path):
        web.seeother('/{0}'.format(path))


class IndexView(BaseView):
    def get(self):
        return com_render.index()
