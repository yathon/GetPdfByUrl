# -*- coding: utf-8 -*-

import os
import time
import base64
from drivers.driver import get_chrome_driver
from config import bconf
from util import time_cost

from reportlab.pdfgen import canvas
from PIL import Image


def __get_doc_title(driver):
    title = driver.find_element_by_xpath('//*[@id="box1"]/div/h1').text

    # 为了兼容windows系统，获取文档标题后转义非法字符
    if bconf['esc_title']:
        for fchar in bconf['forbid_char']:
            title = title.replace(fchar, '_')

    return title


def __make_page_simple(driver):
    js = ''
    # print('隐藏最上边条')
    js = js + 'document.getElementsByClassName(\'header\')[0].style.display="none";'
    # print('隐藏右上角提示')
    js = js + 'document.getElementsByClassName(\'skintips\')[0].style.display="none";'
    # print('隐藏右下角图标集')
    js = js + 'document.getElementsByClassName(\'toplayer-shop\')[0].style.display="none";'
    # print('隐藏文档标题栏-内部')
    # js = js + 'document.getElementsByClassName(\'doctopic\')[0].style.display="none";'
    # print('隐藏文档标题栏')
    js = js + 'document.getElementsByClassName(\'commonbox2 doctopbox\')[0].style.display="none";'
    # print('隐藏工具栏')
    js = js + 'document.getElementsByClassName(\'readshop\')[0].style.display="none";'
    # print('回到页首')
    # js = js + 'document.body.scrollTop=0;'

    driver.execute_script(js)

    # target = driver.find_element_by_class_name('page_view')  # 所有页面载体
    target = driver.find_element_by_class_name('outer_page')  # 单个页面载体

    # print('设置窗口合适大小')
    size = target.size
    driver.set_window_size(size['width'] + 50, size['height'] + 50)
    # driver.set_window_size(50, 50)


@time_cost(bconf['time_cost_type'])
def __get_png_list(url, tmp_path, show_percent=True):
    """
        __get_png_list
    :param url:
    :param tmp_path:
    :return:
    """
    driver = get_chrome_driver()
    driver.get(url)

    # 获取文档标题
    title = __get_doc_title(driver)
    print('文档标题：' + title, flush=True)

    # 获取最大页数
    max_page = int(driver.find_element_by_class_name('text').text[2:])
    if max_page > bconf['max_page'] >= 0:
        max_page = bconf['max_page']
    print('文档页数：' + str(max_page), flush=True)

    # 简化页面
    # __make_page_simple(driver)

    # 获取跳转页面输入框句柄
    page_jump = driver.find_element_by_id('pageNumInput')

    # target = driver.find_element_by_class_name('outer_page')  # 单个页面载体
    # size = target.size
    # size = {'x': size['width'], 'y': size['height']}
    # pdf_name = os.path.join(tmp_path, title + '.pdf')
    # pdf = canvas.Canvas(filename=pdf_name, pagesize=size)

    png_list = []
    for idx in range(1, max_page + 1):
        # 单个页面载体
        pname = 'pagepb_' + str(idx)
        fname = os.path.join(tmp_path, (pname + '.png'))
        if os.path.exists(fname):
            continue
        target = driver.find_element_by_id(pname)

        # print('显示工具栏')
        # js = 'document.getElementsByClassName(\'readshop\')[0].style.display="block";'
        # driver.execute_script(js)
        # 清空并输入需要跳转的页面后触发跳转
        page_jump.clear()
        page_jump.send_keys(str(idx))  # 输入页码
        page_jump.send_keys('\ue007')  # 回车键
        # print('隐藏工具栏')
        # js = 'document.getElementsByClassName(\'readshop\')[0].style.display="none";'
        # driver.execute_script(js)

        # 等待页面加载完成
        print('正在扫描第 ' + str(idx) + ' 页：', end=' ', flush=True)
        for second in range(1, bconf['one_page_wait'] + 1):
            load_percent = target.text
            if load_percent:
                print(load_percent, end=' ', flush=True)
                time.sleep(1)
            else:
                print(r'100%', end=' ', flush=True)
                break
        else:
            print('扫描失败', flush=True)
            driver.quit()

            # 清理缓存文件
            __rm_files(png_list)
            raise Exception('第 ' + str(idx) + ' 页扫描失败，请重试')

        # 跳转元素位置
        # driver.execute_script("arguments[0].scrollIntoView();", target)

        # 截图写入文件
        if bconf['use_png']:
            target.screenshot(fname)
        else:
            js = """
                var canvas = document.getElementById(\'page_%s\');
                dataUrl = canvas.toDataURL();
                return dataUrl;
            """ % idx
            data = driver.execute_script(js).split(',')[1]
            png = base64.b64decode(data.encode('ascii'))

            # pdf.drawImage(png, 0, 0)
            # pdf.showPage()
            with open(fname, 'wb') as f:
                f.write(png)

        # 添加文件列表记录
        png_list.append(fname)
        print('完成', flush=True)

    # pdf.save()
    driver.quit()
    return title, png_list


def __percent(idx, total):
    percent = int((idx / total) * 10000) / 100
    print('%s%%' % str(percent), end=' ', flush=True)
    if percent >= 100:
        print('', flush=True)


@time_cost(bconf['time_cost_type'])
def __make_pdf(fname, plist, show_percent=True):
    """
        __make_pdf
    :param fname:
    :param plist:
    :return:
    """
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
            __percent(idx, cnt)
    pdf.save()


@time_cost(bconf['time_cost_type'])
def __rm_files(flist, show_percent=True):
    """
        __rm_files
    :param flist:
    :return:
    """
    idx = 0
    cnt = len(flist)
    if cnt == 0:
        return

    print('清理缓存', flush=True)
    for f in flist:
        os.remove(f)
        idx = idx + 1
        if show_percent:
            __percent(idx, cnt)


@time_cost(bconf['time_cost_type'])
def doc88_pdf(url, fpath, fname=None, show_percent=True):
    print('开始解析地址：' + url, flush=True)

    if not os.path.exists(fpath):
        print('创建新目录：' + fpath, flush=True)
        os.mkdir(fpath)

    # 获取文档
    title, pngs = __get_png_list(url, fpath, show_percent)
    if title and pngs:
        if fname:
            __make_pdf(os.path.join(fpath, fname + '.pdf'), pngs, show_percent)
        else:
            __make_pdf(os.path.join(fpath, title + '.pdf'), pngs, show_percent)

    # 清理缓存文件
    __rm_files(pngs, show_percent)

    print('文档下载成功', flush=True)

