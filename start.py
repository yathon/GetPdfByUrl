# -*- coding:utf-8 -*-

from config import bconf
from doc88 import doc88_pdf as get_pdf


def start():
    url = r'http://www.doc88.com/p-9005077529870.html'
    # url = r'http://www.doc88.com/p-9119144870919.html'
    fpath = r'/Users/admin/Downloads/doc88/'

    for cnt in range(0, bconf['retry_cnt']):
        try:
            get_pdf(url, fpath)
            break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        start()
    except Exception as ex:
        print(ex)
