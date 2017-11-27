#! -*- coding: utf-8 -*-


import os


from upgradeclient.database.db_wrapper import SqliteMultithread


class Database(object):
    @staticmethod
    def get_base_dir():
        return os.path.dirname(__file__)

    @staticmethod
    def get_client_dir():
        base_dir = Database.get_base_dir()

        return os.path.dirname(base_dir)

    @staticmethod
    def get_project_dir():
        client_dir = Database.get_client_dir()

        return os.path.dirname(client_dir)


__db_name = 'upgradeclient'
__db_conf = (os.path.join(Database.get_base_dir(), '{0}.db'.format(__db_name)), True, 'DELETE')
db = SqliteMultithread(*__db_conf)


