#! -*- coding: utf-8 -*-


import os


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
