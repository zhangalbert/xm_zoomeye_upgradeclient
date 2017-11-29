#! -*- coding: utf-8 -*-


import json


from upgradeclient.domain.model.alert.media import Media
from upgradeclient.domain.model.alert.notify import Notify


class ABS(object):
    def __init__(self, base_url=None, proxy_host=None, target_host=None, revision_seconds=None, summarize_interval=None,
                 auth_user=None, auth_pass=None, notify=None):
        self.base_url = base_url
        self.proxy_host = proxy_host
        self.target_host = target_host
        self.revision_seconds = revision_seconds
        self.summarize_interval = summarize_interval
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.notify = notify

    def get_base_url(self):
        return self.base_url

    def set_base_url(self, base_url):
        self.base_url = base_url

    def get_proxy_host(self):
        return self.proxy_host

    def set_proxy_host(self, proxy_host):
        self.proxy_host = proxy_host

    def get_target_host(self):
        return self.target_host

    def set_target_host(self, target_host):
        self.target_host = target_host

    def get_revision_seconds(self):
        return self.revision_seconds

    def set_revision_seconds(self, revision_seconds):
        self.revision_seconds = revision_seconds

    def get_summarize_interval(self):
        return self.summarize_interval

    def set_summarize_interval(self, summarize_interval):
        self.summarize_interval = summarize_interval

    def get_auth_user(self):
        return self.auth_user

    def set_auth_user(self, auth_user):
        self.auth_user = auth_user

    def get_auth_pass(self):
        return self.auth_pass

    def set_auth_pass(self, auth_pass):
        self.auth_user = auth_pass

    def get_notify(self):
        return self.notify

    def set_notify(self, notify):
        self.notify = notify

    def to_dict(self):
        dict_data = {
            'base_url': self.get_base_url(),
            'proxy_host': self.get_proxy_host(),
            'target_host': self.get_target_host(),
            'revision_seconds': self.get_revision_seconds(),
            'summarize_interval': self.get_summarize_interval(),
            'auth_user': self.get_auth_user(),
            'auth_pass': self.get_auth_pass(),
            'notify': self.get_notify().to_dict()
        }

        return dict_data

    def to_json(self, indent=4):
        dict_data = self.to_dict()
        json_data = json.dumps(dict_data, indent=indent)

        return json_data

    @staticmethod
    def create_notify(dict_data):
        if dict_data is None:
            return None
        medias = dict_data.get('medias', None)
        crontab = dict_data.get('crontab', None)
        if crontab is None or medias is None:
            return None
        notify = Notify(crontab=crontab)
        print '$' * 100
        print medias
        print '$' * 100
        medias_list = []
        for m in medias:
            media = Media(handler=m['handler'], to=m['to'], cc=m['cc'])
            medias_list.append(media)
        notify.set_medias(medias_list)

        return notify



