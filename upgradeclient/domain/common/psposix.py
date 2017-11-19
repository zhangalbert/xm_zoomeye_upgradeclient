#! -*- coding: utf-8 -*-


import os
import errno


class Psposix(object):
    @staticmethod
    def pid_exists(pid):
        if pid == 0:
            return True
        try:
            os.kill(pid, 0)
        except OSError as e:
            if e.errno == errno.ESRCH:
                return False
            if e.errno == errno.EPERM:
                return True
            raise e
        else:
            return True
