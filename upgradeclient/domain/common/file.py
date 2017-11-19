#! -*- coding: utf-8 -*-


import os
import hashlib


class File(object):
    @staticmethod
    def read_content(path):
        f_content = ''
        with open(path, 'r+b') as fd:
            for line in fd:
                f_content += line
        return f_content

    @staticmethod
    def write_content(data, path):
        f_basedir = os.path.dirname(path)
        if not os.path.exists(f_basedir):
            os.makedirs(f_basedir)
        with open(path, 'w+b') as fd:
            fd.write(data)

    @staticmethod
    def dos2unix(path):
        f_content = ''
        with open(path, 'rU') as fd:
            for line in fd:
                f_content += line

        File.write_content(f_content, path)

    @staticmethod
    def get_strs_md5(strs):
        return hashlib.md5(strs).hexdigest()

    @staticmethod
    def get_bigfile_md5(path):
        buffer_size = 4096
        md5 = hashlib.md5()
        with open(path, 'r+b') as fd:
            while True:
                data = fd.read(buffer_size)
                if not data.strip():
                    break
                md5.update(data)

        return md5.hexdigest()

    @staticmethod
    def get_file_md5(path):
        fsize = os.stat(path).st_size
        if fsize > pow(2, 20):
            return File.get_bigfile_md5(path)
        fcontent = File.read_content(path)
        md5 = File.get_strs_md5(fcontent)

        return md5
