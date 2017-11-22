#! -*- coding: utf-8 -*-


import re
import json
import string
import zipfile


from upgradeclient.domain.common.file import File


class Firmware(object):
    @staticmethod
    def release_note2dict(path):
        """ 解析SVN ReleaseNote日志
        """
        date2firmware = {}
        note2firmware = {}
        start_records = False
        # 读取数据,获取以(2016-10-25,IPC_HI3518EV200_50H10L_S38)为键,以后续值为值作为字典
        File.set_file_to_utf8(path)
        with open(path, 'r+b') as rhandler:
            for cur_line in rhandler:
                match = re.match('(\\d{4}-\\d{1,2}-\\d{1,2})\\W+([A-Z-0-9_a-z]+)', cur_line)
                if match:
                    cur_date, cur_type = match.groups()
                    date2firmware.update({(cur_date, cur_type): []})
                    start_records = True
                if start_records:
                    date2firmware[cur_date, cur_type].append(cur_line)

        for cur_key, cur_val in date2firmware.iteritems():
            add_flag = True
            # 长度小于3为错误格式
            if not cur_val[2:]:
                add_flag = False
            # 日期不匹配为错误格式
            if cur_key[0] not in cur_val[2]:
                add_flag = False
            # 日前前有空格错误格式
            if cur_val[2][0] in string.whitespace:
                add_flag = False
            if not add_flag:
                continue

            add_flag = True
            change_dict = {
                'Level': None,
                'XmCloudUpgrade': None,
                'ChangeLog_SimpChinese': [],
                'ChangeLog_English': [],
            }
            for cur_item in cur_val[3:]:
                cur_item = cur_item.rstrip()
                match = re.match('(Level|XmCloudUpgrade|ChangeLog_SimpChinese|ChangeLog_English)\\s*=\\s*(.*)',
                                 cur_item)
                if match:
                    match_key, match_val = match.groups()
                    match_key = match_key.strip()
                    match_val = match_val.strip()
                    if not match_val:
                        match_val = []
                    if match_key == 'Level':
                        if match_val not in ['0', '1']:
                            add_flag = False
                            break
                        change_dict.update({match_key: match_val})
                    if match_key == 'XmCloudUpgrade':
                        if match_val not in ['0', '1']:
                            add_flag = False
                            break
                        change_dict.update({match_key: match_val})
                else:
                    try:
                        change_dict[match_key].append(cur_item)
                    except AttributeError, e:
                        add_flag = False
                        break
            if add_flag:
                note2firmware.update({cur_key: change_dict})

        return note2firmware

    @staticmethod
    def get_devid(path):
        devid = None

        try:
            zfile = zipfile.ZipFile(path, 'r')
        except Exception, e:
            pass
        else:
            for z in zfile.namelist():
                if z == 'InstallDesc':
                    zdata = zfile.read(z)
                    if 'DevID' in zdata:
                        devid = json.loads(zdata)['DevID']

        return devid

    @staticmethod
    def convert_devid(devid):
        resid = None

        if devid is None:
            return resid
        if len(devid) != 24:
            return resid
        if devid[5] < '5':
            resid = devid[:8] + 'XXXXXXXXXXX' + devid[19:]
        else:
            resid = devid[:8] + devid[8:13].replace('2', '0').replace('3', '1') + '0000' + devid[17:]

        return resid
