#! -*- coding: utf-8 -*-


import json


class Event(object):
    def __init__(self, name=None, filename=None, filetype=None, download_url=None, author=None, date=None, number=None,
                 action=None, **_):
        self.name = name
        self.filename = filename
        self.filetype = filetype
        self.download_url = download_url
        self.author = author
        self.date = date
        self.number = number
        self.action = action

    def get_name(self):
        """ 事件名称
        """
        return self.name

    def set_name(self, name):
        self.name = name

    def get_filename(self):
        """ 获取SVN文件名
        """
        return self.filename

    def set_filename(self, filename):
        """ 设置SVN文件名
        """
        self.filename = filename

    def get_filetype(self):
        """ 获取固件类型
        """
        return self.filetype

    def set_filetype(self, filetype):
        """ 设置固件类型
        """
        self.filetype = filetype

    def get_download_url(self):
        """ 获取文件下载地址
        """
        return self.download_url

    def set_download_url(self, download_url):
        """ 设置文件下载地址
        """
        self.download_url = download_url

    def get_author(self):
        """ 获取最后提交者
        """
        return self.author

    def set_author(self, author):
        """ 设置最后提交者
        """
        self.author = author

    def get_date(self):
        """ 获取最近更新日期
        """
        return self.date

    def set_date(self, date):
        """ 设置最近更新日期
        """
        self.date = date

    def get_number(self):
        """ 获取SVN版本号
        """
        return self.number

    def set_number(self, number):
        """ 设置SVN版本号
        """
        self.number = number

    def get_action(self):
        """ 获取文件操作类型
        """
        return self.action

    def set_action(self, action):
        """ 设置文件操作类型
        """
        self.action = action

    def to_dict(self):
        dict_data = {
            "name": self.get_name(),
            'filename': self.get_filename(),
            'filetype': self.get_filetype(),
            'download_url': self.get_download_url(),
            'author': self.get_author(),
            'date': self.get_date(),
            'number': self.get_number(),
            'action': self.get_action(),
        }

        return dict_data

    def to_json(self, indent=4):
        """ 生成JSON事件内容
        """
        dict_data = self.to_dict()
        json_data = json.dumps(dict_data, indent=indent)

        return json_data

    @staticmethod
    def from_json(json_data):
        """ 还原Event事件对象
        """
        dict_data = json.loads(json_data)
        name = dict_data.get('name', None)
        filename = dict_data.get('filename', None)
        filetype = dict_data.get('filetype', None)
        download_url = dict_data.get('download_url', None)
        author = dict_data.get('author', None)
        date = dict_data.get('date', None)
        number = dict_data.get('number', None)
        action = dict_data.get('action', None)

        event = Event(name=name, filename=filename, filetype=filetype, download_url=download_url, author=author,
                      date=date, number=number, action=action)

        return event
