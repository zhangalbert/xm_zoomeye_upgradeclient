#! -*- coding: utf-8 -*-

import os
import web


from upgradeclient.domain.utils.webui.config import template_dir, upgwebui_dir


com_render = web.template.render('{0}/'.format(template_dir), base='layout', cache=False)


class BaseView(object):
    def GET(self, *args, **kwargs):
        raise NotImplementedError

    def POST(self, *args, **kwargs):
        raise NotImplementedError


class StaticFileView(BaseView):
    def GET(self, media, name):
        file_path = os.path.join(upgwebui_dir, 'statics', media, name)
        if not os.path.exists(file_path):
            web.notfound()

        web.header('Content-type', 'application/octet-stream')
        web.header('Transfer-Encoding', 'chunked')
        web.header('Content-Disposition', 'attachment; filename="{0}"'.format(name))
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
    def GET(self, path):
        web.seeother('/{0}'.format(path))


class IndexView(BaseView):
    def GET(self):
        return com_render.index()

