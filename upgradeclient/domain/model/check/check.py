#! -*- coding: utf-8 -*-


import json


from upgradeclient.domain.model.alert.media import Media
from upgradeclient.domain.model.alert.alert import Alert
from upgradeclient.domain.model.upload.upload import Upload


class Check(object):
    def __init__(self, name=None, base_url=None, check_filter=None, proxy_host=None, target_host=None,
                 revision_seconds=None, summarize_interval=None, auth_user=None, auth_pass=None, alert=None,
                 upload=None, target_cache=None):
        self.name = name
        self.alert = alert
        self.upload = upload
        self.base_url = base_url
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.proxy_host = proxy_host
        self.target_host = target_host
        self.check_filter = check_filter
        self.target_cache = target_cache
        self.revision_seconds = revision_seconds
        self.summarize_interval = summarize_interval

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_base_url(self):
        return self.base_url

    def set_base_url(self, base_url):
        self.base_url = base_url

    def get_check_filter(self):
        return self.check_filter

    def set_check_filter(self, check_filter):
        self.check_filter = check_filter

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

    def get_alert(self):
        return self.alert

    def set_alert(self, alert):
        self.alert = alert

    def get_upload(self):
        return self.upload

    def set_upload(self, upload):
        self.upload = upload

    def get_target_cache(self):
        return self.target_cache

    def set_target_cache(self, target_cache):
        self.target_cache = target_cache

    def to_dict(self):
        dict_data = {
            'name': self.get_name(),
            'upload': self.get_upload().to_dict(),
            'base_url': self.get_base_url(),
            'auth_user': self.get_auth_user(),
            'auth_pass': self.get_auth_pass(),
            'alert': self.get_alert().to_dict(),
            'proxy_host': self.get_proxy_host(),
            'target_host': self.get_target_host(),
            'check_filter': self.get_check_filter(),
            'target_cache': self.get_target_cache(),
            'revision_seconds': self.get_revision_seconds(),
            'summarize_interval': self.get_summarize_interval(),
        }

        return dict_data

    def to_json(self, indent=4):
        dict_data = self.to_dict()
        json_data = json.dumps(dict_data, indent=indent)

        return json_data

    @staticmethod
    def create_alert(dict_data):
        if dict_data is None:
            return None
        medias = dict_data.get('medias', None)
        crontab = dict_data.get('crontab', None)
        if crontab is None or medias is None:
            return None
        alert = Alert(crontab=crontab)

        medias_list = []
        for m in medias:
            to, cc = m['to'], m['cc']
            relation_name = m['relation_name']
            relation_type = m['relation_type']
            media = Media(relation_name, relation_type, to, cc)
            medias_list.append(media)
        alert.set_medias(medias_list)

        return alert

    @staticmethod
    def create_upload(list_data):
        if list_data is None:
            return None

        upload_list = []
        for u in list_data:
            relation_name = u['relation_name']
            relation_type = u['relation_type']
            upload = Upload(relation_name, relation_type)
            upload_list.append(upload)

        return upload_list

    @staticmethod
    def from_json(json_data):
        dict_data = json.loads(json_data)
        name = dict_data.get('name', None)
        base_url = dict_data.get('base_url', None)
        auth_user = dict_data.get('auth_user', None)
        auth_pass = dict_data.get('auth_pass', None)
        proxy_host = dict_data.get('proxy_host', None)
        target_host = dict_data.get('target_host', None)
        target_cache = dict_data.get('target_cache', None)
        check_filter = dict_data.get('check_filter', None)
        revision_seconds = dict_data.get('revision_seconds', None)
        summarize_interval = dict_data.get('summarize_interval', None)
        alert = Check.create_alert(dict_data.get('alert', None))
        upload = Check.create_upload(dict_data.get('upload', None))

        check = Check(name=name, base_url=base_url, check_filter=check_filter, proxy_host=proxy_host,
                      target_host=target_host, revision_seconds=revision_seconds, summarize_interval=summarize_interval,
                      auth_user=auth_user, auth_pass=auth_pass, alert=alert, upload=upload, target_cache=target_cache)

        return check


