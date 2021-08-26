# -*- coding: utf-8 -*-
"""
@Time    : 10/20/20 2:38 PM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : customUtils.py
@Desc    : Description about this file
"""
def merge_data(data1, data2):
    '''
    使用data2和data1合并为新的字典
    对于data2和data1都有的key，合成规则为data2的数据覆盖data1
    :param data1
    :param data2
    :return
    '''
    if isinstance(data1, dict) and isinstance(data2, dict):
        new_dict = {}
        d2_keys = list(data2.keys())
        for d1key in data1.keys():
            if d1key in d2_keys:        # data1, data2都有，深度对比
                d2_keys.remove(d1key)
                new_dict[d1key] = merge_data(data1.get(d1key), data2.get(d1key))
            else:
                new_dict[d1key] = data1.get(d1key)      # d1有d2没有的key
        for d2key in d2_keys:
            new_dict[d2key] = data2.get(d2key)
        return new_dict
    else:
        return data2
