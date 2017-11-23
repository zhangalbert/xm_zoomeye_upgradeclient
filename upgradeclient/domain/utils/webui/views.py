#! -*- coding: utf-8 -*-


import web


class RedirectView(object):
    def GET(self, path):
        web.seeother('/{0}'.format(path))


class IndexView(object):
    def GET(self):
        return 'Upgradeclient-Webui, v1.0, author: manmanli'
