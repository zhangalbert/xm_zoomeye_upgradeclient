#! -*- coding: utf-8 -*-

import os
import web


from upgradeclient.domain.utils.webui.config import template_dir, upgwebui_dir


com_render = web.template.render('{0}/'.format(template_dir), base='layout', cache=False)


# class StaticFileView(object):
#     def GET(self, path):
#         file_path = os.path.join(upgwebui_dir, 'statics', path)
#         if not os.path.exists(file_path):
#             web.notfound()
#
#         web.header('Content-type', 'application/octet-stream')
#         web.header('Transfer-Encoding', 'chunked')
#         web.header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(path)))
#         try:
#             with open(file_path, 'r+b') as fd:
#                 while True:
#                     data = fd.read(262144)
#                     if not data:
#                         break
#                     yield data
#         except Exception, e:
#             yield e


class RedirectView(object):
    def GET(self, path):
        web.seeother('/{0}'.format(path))


class IndexView(object):
    def GET(self):
        ls
        return com_render.index()


