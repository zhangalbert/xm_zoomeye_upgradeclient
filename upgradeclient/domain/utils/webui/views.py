#! -*- coding: utf-8 -*-

import os
import web


from upgradeclient.domain.utils.webui.config import template_dir
render = web.template.render('{0}/'.format(template_dir), base=os.path.join(template_dir, 'layout'), cache=False)


class RedirectView(object):
    def GET(self, path):
        web.seeother('/{0}'.format(path))


class IndexView(object):
    def GET(self):
        return render.index()
