#! -*- coding: utf-8 -*-


from upgradeclient.domain.common.filter import Q, R
from upgradeclient.domain.bl.filter.check.base_filter import BaseFilter


class DefaultFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super(DefaultFilter, self).__init__(*args, **kwargs)

    def release_note_validate(self, obj):
        q = super(DefaultFilter, self).release_note_validate(obj) & Q(obj__filetype__not_exact='OEM')

        return R(obj, q_ins=q)()

    def firmware_name_validate(self, obj):
        q = super(DefaultFilter, self).firmware_name_validate(obj)

        return R(obj, q_ins=q)()

