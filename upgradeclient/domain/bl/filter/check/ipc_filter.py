#! -*- coding: utf-8 -*-


from upgradeclient.domain.bl.filter.check.base_filter import BaseFilter


class IpcFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super(IpcFilter, self).__init__(*args, **kwargs)
