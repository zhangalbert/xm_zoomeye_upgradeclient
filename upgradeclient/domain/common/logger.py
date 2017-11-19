#! -*- coding: utf-8 -*-


import logging


class Logger(object):
    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)

        return logger
