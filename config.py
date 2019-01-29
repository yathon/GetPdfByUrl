# -*- coding:utf-8 -*-
__author__ = 'Yathon'
__time__ = '2018/12/14 10:46'

bconf = {
    'max_page': -1,  # 需要下载的页数，-1为下载全部(自动获取最大页数)
    'one_page_wait': 120,  # 每页最大等待下载时间，单位秒
    'time_cost_type': None,  # 打印函数执行耗时，none-忽略，详见下方 tm
    'esc_title': True,  # 标题作为文件名时是否转义非法字符（兼容windows系统必须开启）
    'forbid_char': r' /\:*"<>|?',
    'retry_cnt': 1,  # 重试次数
    'use_png': False,
}

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
