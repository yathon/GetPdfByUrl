# -*- coding:utf-8 -*-
__author__ = 'Yathon'
__time__ = '2018/12/14 10:46'

import os
import functools
import time
from reportlab.pdfgen import canvas
from PIL import Image
from config import bconf, tm, tm_name


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


def percent(idx, total):
    if total:
        perc = int((idx / total) * 10000) / 100
    else:
        perc = 100
    print('%s%%' % str(perc), end=' ', flush=True)
    if perc >= 100:
        print('', flush=True)


@time_cost(bconf['time_cost_type'])
def make_pdf(fname, plist, show_percent=True):
    idx = 0
    cnt = len(plist)
    if cnt == 0:
        return
    print('文件路径为：' + fname, flush=True)
    img = Image.open(plist[0])
    pdf = canvas.Canvas(filename=fname, pagesize=img.size)  # 第一张图片的尺寸新建pdf

    for png in plist:
        pdf.drawImage(png, 0, 0)
        pdf.showPage()
        idx = idx + 1
        if show_percent:
            percent(idx, cnt)
    pdf.save()


@time_cost(bconf['time_cost_type'])
def rm_files(flist, show_percent=True):
    idx = 0
    cnt = len(flist)
    if cnt == 0:
        return
    print('清理缓存', flush=True)
    for f in flist:
        os.remove(f)
        idx = idx + 1
        if show_percent:
            percent(idx, cnt)
