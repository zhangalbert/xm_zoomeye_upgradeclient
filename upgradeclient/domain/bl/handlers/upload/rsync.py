#! -*- coding: utf-8 -*-


import os
import tempfile
import subprocess


from upgradeclient.database.database import Database
from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.bl.handlers.upload.base import BaseHandler


logger = Logger.get_logger(__name__)


class RsyncHandler(BaseHandler):
    def __init__(self, cache=None):
        super(RsyncHandler, self).__init__(cache=cache)

    def setmode(self, path, mode):
        if not os.path.exists(path) or not str(mode).isdigit():
            return
        oct_mode = int(str(mode), 8)
        os.chmod(path, oct_mode)

    def set_password(self, obj):
        authdir = os.path.join(Database.get_client_dir(), 'auth', 'rsync')
        password_file = os.path.join(authdir, '{0}.password'.format(obj.get_serverip()))
        self.setmode(password_file, 600)
        obj.set_password(password_file)

    def set_localpath(self, obj):
        obj.set_localpath(os.path.join(self.cache.base_path, obj.get_localpath()))

    def command(self, obj):
        execute_command = []

        self.set_password(obj)
        self.set_localpath(obj)

        execute_command.append(obj.get_binpath())
        execute_command.append('-avzut')
        execute_command.append('--progress')
        execute_command.append('--password-file={0}'.format(obj.get_password()))
        execute_command.append(obj.get_localpath()),
        execute_command.append('{0}@{1}::{2}'.format(obj.get_username(), obj.get_serverip(), obj.get_remotepath()))

        return ' '.join(execute_command)

    def execute(self, command):
        output = tempfile.NamedTemporaryFile(mode='a+b')
        p = subprocess.Popen(command, stdout=output, stderr=output, shell=True, close_fds=True)
        current_position = 0
        with open(output.name) as fd:
            while True:
                output.file.flush()
                fd.seek(current_position)
                line = fd.readline()
                if line.strip():
                    logger.debug(line)
                current_position = fd.tell()
                if p.poll() is not None:
                    break
        return p.returncode == 0

    def handle(self, obj):
        command = self.command(obj)
        logger.debug('upload service start {0}'.format(command))
        if self.execute(command) is True:
            logger.info('{0} execute successfully'.format(command))
        else:
            logger.error('{0} execute failed'.format(command))
