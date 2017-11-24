#! -*- coding: utf-8 -*-

import os
import logging


from upgradeclient.database.database import Database


template_dir = os.path.join(Database.get_client_dir(), 'domain', 'utils', 'webui', 'templates')

env = {
    # 至少一处理器
    'log': True,
    'logmessage': 'web.py server got itself in trouble',
    'logname': 'web.py',
    'loglevel': logging.DEBUG,
    'logformat': '%(name)s:  %(asctime)s %(levelname)-4s %(message)s',
    'datefmt': '%a, %d %b %Y %H: %M: %S',
    'tostream': True,
    'prnlevel': logging.DEBUG,

    # 是否开启调试
    'debug': True,

    # 输出HTML错误
    'tohtml': True,
    'htmlfile': os.path.join(template_dir, 'error.html')
}
