#! -*- coding: utf-8 -*-


import os


from functools import partial


from upgradeclient.database.database import db


class BaseHandler(object):
    def __init__(self, cache=None, dao_factory=None):
        self.cache = cache
        self.dao_factory = dao_factory
        self.event_type = None

    def insert(self, obj):
        parted_dict = {
            'log_name': self.event_type,
            'log_class': self.__class__.__name__,
            'file_type': obj.get_filetype() or '',
            'file_name': obj.get_filename() or '',
            'file_url': obj.get_download_url() or '',
            'last_author': obj.get_author() or '',
            'last_date': obj.get_date() or '',
            'last_revision': obj.get_number() or '',
            'last_action': obj.get_action() or '',
        }

        return partial(db.insert, **parted_dict)

    def delete(self, *files):
        for f in files:
            if not os.path.exists(f):
                continue
            os.remove(f)

    def handle(self, obj):
        raise NotImplementedError

