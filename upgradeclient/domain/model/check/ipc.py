#! -*- coding: utf-8 -*-


import json


from upgradeclient.domain.model.check.abs import ABS


class IPC(ABS):
    NAME = 'ipc'

    def __init__(self, base_url=None, proxy_host=None, target_host=None, revision_seconds=None, summarize_interval=None,
                 auth_user=None, auth_pass=None, notify=None):
        super(IPC, self).__init__(base_url=base_url, proxy_host=proxy_host, target_host=target_host,
                                  revision_seconds=revision_seconds, summarize_interval=summarize_interval,
                                  auth_user=auth_user, auth_pass=auth_pass, notify=notify)

    @staticmethod
    def from_json(json_data):
        all_dict = json.loads(json_data)
        if IPC.NAME in all_dict:
            dict_data = all_dict[IPC.NAME]
        else:
            dict_data = all_dict

        base_url = dict_data.get('base_url', None)
        proxy_host = dict_data.get('proxy_host', None)
        target_host = dict_data.get('target_host', None)
        revision_seconds = dict_data.get('revision_seconds', None)
        summarize_interval = dict_data.get('summarize_interval', None)
        auth_user = dict_data.get('auth_user', None)
        auth_pass = dict_data.get('auth_pass', None)
        notify = ABS.create_notify(dict_data.get('notify', None))

        ipc = IPC(base_url=base_url, proxy_host=proxy_host, target_host=target_host, revision_seconds=revision_seconds,
                  summarize_interval=summarize_interval, auth_user=auth_user, auth_pass=auth_pass, notify=notify)

        return ipc

