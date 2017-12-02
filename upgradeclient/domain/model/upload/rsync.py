#! -*- coding: utf-8 -*-


import json


class Rsync(object):
    NAME = 'rsync'

    def __init__(self, binpath=None, localpath=None, username=None, serverip=None, serverport=None, remotepath=None, password=None):
        self.binpath = binpath
        self.username = username
        self.serverip = serverip
        self.password = password
        self.localpath = localpath
        self.serverport = serverport
        self.remotepath = remotepath

    def get_binpath(self):
        return self.binpath

    def set_binpath(self, binpath):
        self.binpath = binpath

    def get_localpath(self):
        return self.localpath

    def set_localpath(self, localpath):
        self.localpath = localpath

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_serverip(self):
        return self.serverip

    def set_serverip(self, serverip):
        self.serverip = serverip

    def get_serverport(self):
        return self.serverport

    def set_serverport(self, serverport):
        self.serverport = serverport

    def get_remotepath(self):
        return self.remotepath

    def set_remotepath(self, remotepath):
        self.remotepath = remotepath

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_remoteurl(self):
        fmtdata = (Rsync.NAME, self.get_username(), self.get_serverip(), self.get_serverport(),
                   self.get_localpath(), self.remotepath)
        return '{0}://{1}@{2}:{3}/{4} {5}'.format(*fmtdata)

    def to_dict(self):
        dict_data = {
            'binpath': self.get_binpath(),
            'localpath': self.get_localpath(),
            'username': self.get_username(),
            'serverip': self.get_serverip(),
            'serverport': self.get_serverport(),
            'remotepath': self.get_remotepath(),
            'password': self.get_password()
        }

        return dict_data

    def to_json(self):
        dict_data = self.to_dict()
        json_data = json.dumps(dict_data)

        return json_data

    @staticmethod
    def from_json(json_data):
        dict_data = json.loads(json_data)

        binpath = dict_data.get('binpath', None)
        localpath = dict_data.get('localpath', None)
        username = dict_data.get('username', None)
        serverip = dict_data.get('serverip', None)
        serverport = dict_data.get('serverport', None)
        remotepath = dict_data.get('remotepath', None)
        password = dict_data.get('password', None)

        rsync = Rsync(binpath=binpath, localpath=localpath, username=username, serverport=serverport, serverip=serverip,
                      remotepath=remotepath, password=password)

        return rsync
