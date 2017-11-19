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

    def to_revision_date(self, timetuple):
        timestamp = time.mktime(timetuple)
        revision_date = pysvn.Revision(pysvn.opt_revision_kind.date, timestamp)

        return revision_date

    def info(self, url, *args, **kwargs):
        svn_info = self.svnclient.info2(url, *args, **kwargs)[0][-1]
        data = {
            'date': svn_info.last_changed_date,
            'author': svn_info.last_changed_author,
            'number': svn_info.rev.number if svn_info.rev else svn_info.rev,
        }

        return data

    def revision_summarize(self, url, sta_timetuple, end_timetuple):
        revision_min, revision_max = map(lambda t: self.to_revision_date(t), (sta_timetuple, end_timetuple))
        summarizes = self.svnclient.diff_summarize(url, revision_min, url, revision_max)

        latest_changes = []
        for item in summarizes:
            file_kind = pysvn.node_kind.file
            file_path = item['path']
            node_kind = item['node_kind']
            if file_kind != node_kind:
                continue
            full_url = urlparse.urljoin(url, file_path)
            full_url = urllib.quote(full_url.encode('utf-8'), safe=':/')
            svn_info = self.info(full_url)
            filename = '_'.join([os.path.basename(full_url), svn_info['number']])
            svn_info.update({
                'filename': ExtStr(filename),
                'download_url': ExtStr(full_url)
            })
            print '='*100
            print svn_info
            print '='*100
            latest_changes.append(svn_info)

        return latest_changes
