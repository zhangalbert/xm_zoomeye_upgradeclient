#! -*- coding: utf-8 -*-


import os
import web


from functools import partial


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


__polling = True
__db_name = 'upgradeclient'
__db_path = os.path.join(Database.get_base_dir(), '{0}.db'.format(__db_name))
# sqlite3多线程异步写入需要DButils模块支持
db = web.database(dbn='sqlite', db=__db_path, pooling=__polling)
db.select = partial(db.select, __db_name)
db.update = partial(db.update, __db_name)
db.delete = partial(db.delete, __db_name)
db.insert = partial(db.insert, __db_name)
