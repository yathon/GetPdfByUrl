# -*- coding:utf-8 -*-

import functools
import time
from config import tm, tm_name


def time_cost(tm_type='msec'):
    """
        time_cost
    :param tm_type: 'usec'-微秒，'msec'-毫秒，'sec'-秒，'min'-分钟
    :return:
    """
    def __derorator(func):
        @functools.wraps(func)
        def __wrapper(*args, **kwargs):
            if tm_type:
                begin = time.time()
                rst = func(*args, **kwargs)
                end = time.time()
                print('函数[%s]耗时[%s]%s' % (func.__name__, str((end - begin) * tm[tm_type]), tm_name[tm_type]))
            else:
                rst = func(*args, **kwargs)

            return rst
        return __wrapper
    return __derorator
