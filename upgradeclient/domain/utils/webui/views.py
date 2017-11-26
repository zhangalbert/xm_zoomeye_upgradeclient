#! -*- coding: utf-8 -*-

import os
import web
import json


from upgradeclient.database.database import db
from upgradeclient.domain.utils.webui.config import template_dir, upgwebui_dir


com_render = web.template.render('{0}/'.format(template_dir), base='layout', cache=False)


class BaseView(object):
    def json_response(self, data):
        web.header('Content-type', 'application/json')

        return json.dumps(data, indent=4)

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


class ExceptionThreadView(BaseView):
    def GET(self):
        pass


class ExceptionFmodelView(BaseView):
    def GET(self):
        pass


class ExceptionExceptView(BaseView):
    def GET(self):
        pass


class ExceptionRealtimeView(BaseView):
    def GET(self):
        response_data = []

        loglevels = ['info', 'warning', 'error']
        input_storage = web.input(limit=20, log_level='error')
        log_limit = input_storage.limit
        log_level = loglevels[loglevels.index(input_storage.log_level):]

        where_con = ' or '.join(map(lambda s: 'log_level=\'{0}\''.format(s), log_level))

        select_storage = db.select(where=where_con, limit=log_limit, order='created_time desc')
        for ins in select_storage:
            response_data.append({
                'id': ins.id,
                'log_level': ins.log_level,
                'log_name': ins.log_name,
                'log_class': ins.log_class,
                'dao_name': ins.dao_name,
                'file_type': ins.file_type,
                'file_name': ins.file_name,
                'file_url': ins.file_url,
                'last_author': ins.last_author,
                'last_date': ins.last_date,
                'last_revision': ins.last_revision,
                'last_action': ins.last_action,
                'log_message': ins.log_message,
                'created_date': ins.created_time.strftime('%Y-%m-%d'),
                'created_time': ins.created_time.strftime('%H-%M-%S')
            })

        return self.json_response(response_data)


