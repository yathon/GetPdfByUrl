# -*- coding:utf-8 -*-
__author__ = 'Yathon'
__time__ = '2018/12/14 10:46'

import traceback
from config import bconf
from doc88 import doc88_pdf as get_pdf


def start():
    # url = r'http://www.doc88.com/p-9005077529870.html'
    # url = r'http://www.doc88.com/p-9119144870919.html'
    url = r'http://www.doc88.com/p-1512873714334.html'
    fpath = r'/Users/admin/Downloads/doc88/'

    for cnt in range(0, bconf['retry_cnt']):
        try:
            get_pdf(url, fpath)
            break
        except Exception as e:
            print(e, flush=True)
            print('文档下载失败，文档已删除或网络错误', flush=True)
            print(traceback.format_exc(), flush=True)


if __name__ == '__main__':
    try:
        start()
    except Exception as ex:
        print(ex)
