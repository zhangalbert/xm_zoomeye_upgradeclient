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


class StaticFileView(BaseView):
    def get(self, relative_path, file):
        file_path = os.path.join(template_dir, relative_path, file)
        if not os.path.exists(file_path):
            web.notfound()

        web.header('Content-type', 'application/octet-stream')
        web.header('Transfer-Encoding', 'chunked')
        web.header('Content-Disposition', 'attachment; filename="{0}"'.format(file))
        try:
            with open(file_path, 'r+b') as fd:
                while True:
                    data = fd.read(262144)
                    if not data:
                        break
                    yield data
        except Exception, e:
            yield e


class RedirectView(BaseView):
    def get(self, path):
        web.seeother('/{0}'.format(path))


class IndexView(BaseView):
    def get(self):
        return com_render.index()

