#! -*- coding: utf-8 -*-


class Helper(object):
    @staticmethod
    def string_escape(strs):
        return strs.replace("'", '"')

    @staticmethod
    def combin_sql_conditions(s='and', conditions=[]):
        condition_list = []
        for k, v in conditions:
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

