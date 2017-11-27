#! -*- coding: utf-8 -*-


class Helper(object):
    @staticmethod
    def combin_sql_conditions(s='and', **kwargs):
        condition_list = []
        for k, v in kwargs.iteritems():
            if len(condition_list) > 0:
                condition_list.append('{0} {1}=\'{2}\''.format(s, k, v))
                continue
            condition_list.append('{0}=\'{1}\''.format(k, v))

        return condition_list

    @staticmethod
    def combin_sql_values(*args):
        condition_list = []
        for k in args:
            condition_list.append('\'{0}\''.format(k))

        return condition_list
