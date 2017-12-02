#! -*- coding: utf-8 -*-


import os


from upgradeclient.domain.common.file import File
from upgradeclient.domain.common.filter import Q, R
from upgradeclient.domain.utils.extstr import ExtStr
from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.utils.download import Download
from upgradeclient.domain.utils.firmware import Firmware
from upgradeclient.domain.model.event.event_type import EventType
from upgradeclient.domain.bl.handlers.download.base import BaseHandler


logger = Logger.get_logger(__name__)


class FirmwareHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(FirmwareHandler, self).__init__(*args, **kwargs)
        self.event_type = EventType.downloading_firmware

    def create_files(self, dict_data, relative_path):
        return_res = {'is_success': True, 'error': ''}

        tdirname = os.path.join(self.cache.base_path, 'download_cache')
        dst_name = os.path.join(tdirname, os.path.basename(dict_data['Firmware'].relative_path))
        upgdevid = Firmware.convert_devid(Firmware.get_devid(dst_name))
        if upgdevid is None:
            return_res = {'is_success': False, 'error': 'invalid devid in InstallDesc'}
            return return_res

        upgfiles = os.path.join(self.cache.base_path, relative_path, upgdevid)
        for k, v in dict_data.iteritems():
            if getattr(v, 'relative_path', None) is not None and getattr(v, 'file_contents', None):
                path = os.path.join(upgfiles, v.relative_path)
                data = v.file_contents
                if os.path.exists(path) and File.get_file_md5(path) == File.get_strs_md5(data):
                    continue
                File.write_content(data, path)

        return return_res

    def is_allow_gen(self, obj):
        q = Q(obj__ChangeLog_SimpChinese__file_contents__not_exact='') & \
            Q(obj__ChangeLog_English__file_contents__not_exact='') & \
            Q(obj__Level__file_contents__not_exact='1') & \
            Q(obj__XmCloudUpgrade__exact='1')

        return R(obj, q_ins=q)()

    def analysis_log(self, obj):
        tdirname = os.path.join(self.cache.base_path, 'download_cache')
        fsrcname = obj.get_filename().rsplit('_', 1)[0]
        dst_name = os.path.join(tdirname, fsrcname)

        eventdata = obj.get_data()
        eventdata['ChangeLog_SimpChinese'] = type('obj', (object,), {
            'relative_path': ExtStr(os.path.join(eventdata['Date'], 'ChangeLog_SimpChinese.dat')),
            'file_contents': ExtStr(os.linesep.join(eventdata['ChangeLog_SimpChinese']).strip()),
        })
        eventdata['ChangeLog_English'] = type('obj', (object,), {
            'relative_path': ExtStr(os.path.join(eventdata['Date'], 'ChangeLog_English.dat')),
            'file_contents': ExtStr(os.linesep.join(eventdata['ChangeLog_English']).strip()),
        })
        eventdata['Level'] = type('obj', (object,), {
            'relative_path': ExtStr(os.path.join(eventdata['Date'], 'Level_{0}.dat'.format(eventdata['Level']))),
            'file_contents': ExtStr(eventdata['Level'].strip()),
        })
        eventdata['Firmware'] = type('obj', (object,), {
            'relative_path': ExtStr(os.path.join(eventdata['Date'], fsrcname)),
            'file_contents': ExtStr(open(dst_name, 'r+b').read()).strip(),
        })
        eventdata['XmCloudUpgrade'] = ExtStr(eventdata['XmCloudUpgrade'])

        event_obj = type('obj', (object,), eventdata)
        if not self.is_allow_gen(event_obj):
            return None

        return eventdata

    def handle(self, obj):
        filename = obj.get_filename()
        file_url = obj.get_download_url()

        sdirname = os.path.join(self.cache.base_path, 'check_cache')
        tdirname = os.path.join(self.cache.base_path, 'download_cache')
        fsrcname = filename.rsplit('_', 1)[0]
        src_name = os.path.join(sdirname, filename)
        dst_name = os.path.join(tdirname, fsrcname)

        download = Download()
        download_res = download.wget(file_url, dst_name)
        if download_res['is_success'] is False:
            fmtdata = (self.__class__.__name__, filename, download_res['error'], file_url)
            msgdata = '{0} download {1} with exception, exp={2} url={3}'.format(*fmtdata)
            self.insert_to_db(obj, log_level='error', log_message=msgdata)
            logger.error(msgdata)
            return

        eventdata = obj.get_data()
        dict_data = self.analysis_log(obj)
        if dict_data is None:
            self.delete(src_name, dst_name)
            fmtdata = (self.__class__.__name__, eventdata['Date'], file_url)
            msgdata = '{0} delected unallowed condition in releasenote {1} log, url={2}'.format(*fmtdata)
            self.insert_to_db(obj, log_level='error', log_message=msgdata)
            logger.error(msgdata)
            return

        dao_data = self.get_dao_data(obj)
        relative_path = os.path.join('upgrade_files', dao_data.get_target_cache())
        create_res = self.create_files(dict_data, relative_path)
        if create_res['is_success'] is False:
            self.delete(src_name, dst_name)
            fmtdata = (self.__class__.__name__, filename, create_res['error'], file_url)
            msgdata = '{0} delected {1} with error, err={2}, url={3}'.format(*fmtdata)
            self.insert_to_db(obj, log_level='error', log_message=msgdata)
            logger.error(msgdata)
            return

        self.delete(src_name, dst_name)
