#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.filter import Q, R


class BaseFilter(object):
    def release_note_validate(self, obj):
        q = Q(obj__filename__regexp='^ReleaseNote') & \
            Q(obj__download_url__regexp=r'ReleaseNote$') & \
            Q(obj__filetype__not_exact='OEM')

        return R(obj, q_ins=q)()
