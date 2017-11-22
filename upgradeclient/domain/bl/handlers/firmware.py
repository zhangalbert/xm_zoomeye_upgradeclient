#! -*- coding: utf-8 -*-


import os


from upgradeclient.domain.common.file import File
from upgradeclient.domain.common.filter import Q, R
from upgradeclient.domain.utils.extstr import ExtStr
from upgradeclient.domain.common.logger import Logger
from upgradeclient.domain.utils.download import Download
from upgradeclient.domain.utils.firmware import Firmware
from upgradeclient.domain.bl.handlers.base import BaseHandler


logger = Logger.get_logger(__name__)


class FirmwareHandler(BaseHandler):
    def create_files(self, obj):
        is_created = True

        upgfiles = os.path.join(self.cache.base_path, 'upgrade_files')
        tdirname = os.path.join(self.cache.base_path, 'download_cache')
        dst_name = os.path.join(tdirname, os.path.basename(obj['Firmware'].relative_path))
        upgdevid = Firmware.convert_devid(Firmware.get_devid(dst_name))
        if upgdevid is None:
            is_created = False
            return is_created

        for k, v in obj.iteritems():
            if getattr(v, 'relative_path', None) is not None and getattr(v, 'file_contents', None):
                path = os.path.join(upgfiles, v.relative_path)
                data = v.file_contents
                File.write_content(data, path)

        return is_created

    def is_allow_gen(self, obj):
        q = Q(obj__ChangeLog_SimpChinese__not_exact='') & \
            Q(obj__ChangeLog_English__not_exact='') & \
            Q(obj__Level__not_exact='1') & \
            Q(obj__XmCloudUpgrade__exact='1')

        return R(obj, q_ins=q)()

    def analysis_log(self, obj):
        tdirname = os.path.join(self.cache.base_path, 'download_cache')
        fsrcname = obj.get_filename().rsplit('_', 1)[0]
        dst_name = os.path.join(tdirname, fsrcname)

        eventdata = obj.get_data()
        eventdata['ChangeLog_SimpChinese'] = type('obj', (ExtStr,), {
            'relative_path': ExtStr(os.path.join(eventdata['Date'], 'ChangeLog_SimpChinese.dat')),
            'file_contents': ExtStr(os.linesep.join(eventdata['ChangeLog_SimpChinese']).strip()),
        })
        eventdata['ChangeLog_English'] = type('obj', (ExtStr,), {
            'relative_path': ExtStr(os.path.join(eventdata['Date'], 'ChangeLog_English.dat')),
            'file_contents': ExtStr(os.linesep.join(eventdata['ChangeLog_English']).strip()),
        })
        eventdata['Level'] = type('obj', (ExtStr,), {
            'relative_path': ExtStr(os.path.join(eventdata['Date'], 'Level_{0}.dat'.format(eventdata['Level']))),
            'file_contents': ExtStr(eventdata['Level'].strip()),
        })
        eventdata['Firmware'] = type('obj', (ExtStr,), {
            'relative_path': ExtStr(os.path.join(eventdata['Date'], fsrcname)),
            'file_contents': ExtStr(open(dst_name, 'r+b').read()).strip(),
        })
        eventdata['XmCloudUpgrade'] = ExtStr(eventdata['XmCloudUpgrade'])
        event_obj = type('obj', (object,), eventdata)
        if not self.is_allow_gen(event_obj):
            return None

        return eventdata

    def handle(self, obj):
        """ 处理DOWNLOADING_FIRMWARE事件
        1. 下载.bin文件到download_cache
        2. 下载成功调用analysis_log解析event_data数据并创建指定升级目录
        3. 结束后删除download_cache内对应的任务
        """
        file_url = obj.get_download_url()
        sdirname = os.path.join(self.cache.base_path, 'check_cache')
        tdirname = os.path.join(self.cache.base_path, 'download_cache')
        fsrcname = obj.get_filename().rsplit('_', 1)[0]
        src_name = os.path.join(sdirname, obj.get_filename())
        dst_name = os.path.join(tdirname, fsrcname)

        download = Download()
        if not download.wget(obj.get_download_url(), dst_name):
            return
        eventdata = self.analysis_log(obj)
        if eventdata is None:
            self.delete(src_name, dst_name)
            logger.error('firmware releasenote with unallowed condition, url={0}'.format(file_url))
            return
        if not self.create_files(eventdata):
            self.delete(src_name, dst_name)
            logger.error('firmware devid in InstallDesc with unallowed condition, url={0}'.format(file_url))
            return
        self.delete(src_name, dst_name)




