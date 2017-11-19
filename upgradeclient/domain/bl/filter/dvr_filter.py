#! -*- coding: utf-8 -*-


from upgradeclient.domain.bl.filter.base_filter import BaseFilter


class DvrFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super(DvrFilter, self).__init__(*args, **kwargs)
