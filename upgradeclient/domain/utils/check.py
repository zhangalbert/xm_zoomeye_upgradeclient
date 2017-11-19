#! -*- coding: utf-8 -*-


import os
import time
import pysvn
import urllib
import urlparse


from upgradeclient.domain.common.file import File
from upgradeclient.domain.utils.extstr import ExtStr


class Check(object):
    def __init__(self):
        self.svnclient = pysvn.Client()

    def auth(self, username, password):
        self.svnclient.set_default_username(username)
        self.svnclient.set_default_password(password)

    def set_commit_info_style(self, style_num=1):
        """
        1. 0 int  revision
        2. 1 dict date, author, revision and post_commit_err
        """
        self.svnclient.commit_info_style = style_num

    def reg_callback_notify(self, func=None):
        if func is not None:
            self.svnclient.callback_notify = func

    def reg_login_callback(self, func=lambda *args: (True, None, None, False)):
        self.svnclient.callback_get_login = func

    def timestamp2revision_date(self, timestamp):
        revision_date = pysvn.Revision(pysvn.opt_revision_kind.date, timestamp)

        return revision_date

    def revision_summarize(self, url, start_timestamp, end_timestamp=time.time()):
        revision_min, revision_max = map(lambda t: self.timestamp2revision_date(t), (start_timestamp, end_timestamp))
        summarizes = self.svnclient.diff_summarize(url, revision_min, url, revision_max)

        print url, revision_min, revision_max, summarizes
        latest_changes = []
        for item in summarizes:
            file_kind = pysvn.node_kind.file
            file_path = item['path']
            node_kind = item['node_kind']
            if file_kind != node_kind:
                continue
            full_url = urlparse.urljoin(url, file_path)
            full_url = urllib.quote(full_url.encode('utf-8'), safe=':/')
            urls_md5 = File.get_strs_md5(full_url)
            name_md5 = '_'.join([os.path.basename(full_url), urls_md5])

            latest_changes.append({'filename': ExtStr(name_md5), 'download_url': ExtStr(full_url)})

        return latest_changes