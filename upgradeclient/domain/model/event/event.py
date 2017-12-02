#! -*- coding: utf-8 -*-


import json


class Event(object):
    def __init__(self, name=None, filename=None, filetype=None, download_url=None, author=None, date=None, number=None,
                 action=None, daoname=None, data=None, **_):
        self.name = name
        self.date = date
        self.number = number
        self.action = action
        self.author = author
        self.daoname = daoname
        self.filetype = filetype
        self.filename = filename
        self.download_url = download_url



        self.data = data

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename

    def get_daoname(self):
        return self.daoname

    def set_daoname(self, daoname):
        set.daoname = daoname

    def get_filetype(self):
        return self.filetype

    def set_filetype(self, filetype):
        self.filetype = filetype

    def get_download_url(self):
        return self.download_url

    def set_download_url(self, download_url):
        self.download_url = download_url

    def get_author(self):
        return self.author

    def set_author(self, author):
        self.author = author

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

    def get_action(self):
        return self.action

    def set_action(self, action):
        self.action = action

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def to_dict(self):
        dict_data = {
            'data': self.get_data(),
            "name": self.get_name(),
            'date': self.get_date(),
            'author': self.get_author(),
            'action': self.get_action(),
            'number': self.get_number(),
            'daoname': self.get_daoname(),
            'filetype': self.get_filetype(),
            'filename': self.get_filename(),
            'download_url': self.get_download_url(),
        }

        return dict_data

    def to_json(self, indent=4):
        dict_data = self.to_dict()
        json_data = json.dumps(dict_data, indent=indent)

        return json_data

    @staticmethod
    def from_json(json_data):
        dict_data = json.loads(json_data)

        date = dict_data.get('date', None)
        name = dict_data.get('name', None)
        data = dict_data.get('data', None)
        author = dict_data.get('author', None)
        number = dict_data.get('number', None)
        action = dict_data.get('action', None)
        daoname = dict_data.get('daoname', None)
        filename = dict_data.get('filename', None)
        filetype = dict_data.get('filetype', None)
        download_url = dict_data.get('download_url', None)

        event = Event(name=name, filename=filename, filetype=filetype, download_url=download_url, author=author,
                      date=date, number=number, action=action, daoname=daoname, data=data)

        return event
