# -*- coding:utf-8 -*-

import functools
import time


def time_cost(time_type='msec'):
    """
        time_cost
    :param time_type: 'usec'-微秒，'msec'-毫秒，'sec'-秒，'min'-分钟
    :return:
    """
    tm = {
        'usec': 1000000.00,
        'msec': 1000.00,
        'sec': 1.00,
        'min': 0.01666667,
    }
    tm_name = {
        'usec': '微秒',
        'msec': '毫秒',
        'sec': '秒',
        'min': '分钟',
    }

    def __derorator(func):
        @functools.wraps(func)
        def __wrapper(*args, **kwargs):
            if time_type:
                begin = time.time()
                rst = func(*args, **kwargs)
                end = time.time()
                print('函数[%s]耗时[%s]%s' % (func.__name__, str((end - begin) * tm[time_type]), tm_name[time_type]))
            else:
                rst = func(*args, **kwargs)

            return rst
        return __wrapper
    return __derorator
