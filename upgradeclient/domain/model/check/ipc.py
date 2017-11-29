#! -*- coding: utf-8 -*-


import json


from upgradeclient.domain.model.check.abs import ABS
from upgradeclient.domain.common.logger import Logger


logger = Logger.get_logger(__name__)


class IPC(ABS):
    NAME = 'ipc'

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
        logger.error(dict_data.get('notify', None))
        notify = ABS.create_notify(dict_data.get('notify', None))
        logger.error(notify)


        ipc = IPC(base_url=base_url, proxy_host=proxy_host, target_host=target_host, revision_seconds=revision_seconds,
                  summarize_interval=summarize_interval, auth_user=auth_user, auth_pass=auth_pass, notify=notify)

        return ipc

