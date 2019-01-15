# -*- coding: utf-8 -*-

import os
import time
from drivers.driver import get_chrome_driver
from config import bconf
from util import time_cost

from reportlab.pdfgen import canvas
from PIL import Image


@time_cost(bconf['time_cost_type'])
def __get_doc_title(driver):
    """
        __get_doc_title
    :param driver:
    :return:
    """
    title = driver.find_element_by_class_name('doctopic')
    title = title.find_element_by_xpath('h1').text
    # print('文档标题：' + title)

    # 为了兼容windows系统，获取文档标题后转义非法字符
    if bconf['esc_title']:
        for fchar in bconf['forbid_char']:
            title = title.replace(fchar, '_')

    return title


@time_cost(bconf['time_cost_type'])
def __make_page_simple(driver):
    """
        __make_page_simple
    :param driver:
    :return:
    """
    # print('页面全屏')
    fullscreen = driver.find_element_by_id('frscreen')
    fullscreen.click()

    # print('放大页面')
    # bigger = driver.find_element_by_id('zoomInButton')
    # for cnt in range(1, 8):
    #     bigger.click()
    #     time.sleep(0.3)

    # print('隐藏工具选项栏')
    # js = 'document.getElementsByClassName(\'readshop\')[0].style.display="none";'
    # driver.execute_script(js)

    # print('隐藏最上边条')
    # print('隐藏右上角提示')
    # print('隐藏右下角图标集')
    # print('隐藏工具栏上所有项目（保留输入框）')
    js = '''
    document.getElementsByClassName(\'header\')[0].style.display="none";
    document.getElementsByClassName(\'skintips\')[0].style.display="none";
    document.getElementsByClassName(\'toplayer-shop\')[0].style.display="none";
    document.getElementsByClassName(\'shop1\')[2].style.display="none";
    document.getElementsByClassName(\'shop2\')[0].style.display="none";
    document.getElementById('prePageButton').style.display="none";
    document.getElementById('nextPageButton').style.display="none";
    document.getElementsByClassName(\'shop4\')[0].style.display="none";
    document.getElementsByClassName(\'shop4\')[0].style.display="none";
    document.getElementsByClassName(\'shop4 share\')[0].style.display="none";
    '''
    driver.execute_script(js)

    # print('设置窗口合适大小')
    page_size = driver.find_element_by_class_name('outer_page')
    # print(page_size.size)
    driver.set_window_size(page_size.size['width'] + 20, page_size.size['height'] + 10)


@time_cost(bconf['time_cost_type'])
def __get_png_list(url, tmp_path):
    """
        __get_png_list
    :param url:
    :param tmp_path:
    :return:
    """
    png_list = []

    # print('Init Chrome')
    driver = get_chrome_driver()

    # print('Starting to get page')
    driver.get(url)

    # 获取文档标题
    title = __get_doc_title(driver)
    print('文档标题：' + title)

    # 获取最大页数
    max_page = int(driver.find_element_by_class_name('text').text[2:])
    if max_page > bconf['max_page'] >= 0:
        max_page = bconf['max_page']
    print('文档页数：' + str(max_page))

    # 隐藏多余元素并将页面放大
    __make_page_simple(driver)

    # 获取跳转页面输入框句柄
    page_num_input = driver.find_element_by_id('pageNumInput')

    # print('Starting to snap page')
    for idx in range(1, max_page + 1):
        # 显示工具选项栏
        # js = 'document.getElementsByClassName(\'readshop\')[0].style.display="block";'
        # driver.execute_script(js)

        # 清空并输入需要跳转的页面后触发跳转
        page_num_input.clear()
        page_num_input.send_keys(str(idx))  # 输入页码
        page_num_input.send_keys('\ue007')  # 输入回车

        # 隐藏工具选项栏
        # js = 'document.getElementsByClassName(\'readshop\')[0].style.display="none";'
        # driver.execute_script(js)

        # 等待页面加载完成
        print('正在下载第 ' + str(idx) + ' 页：', end=' ', flush=True)
        for second in range(1, bconf['one_page_wait'] + 1):
            load_percent = driver.find_element_by_id('pagepb_' + str(idx)).text
            if load_percent:
                time.sleep(1)
                print(load_percent, end=' ', flush=True)
            else:
                break
        else:
            print('下载失败')
            driver.quit()
            __rm_files(png_list)
            raise Exception('第 ' + str(idx) + ' 页下载失败，请重试')

        # print('Write to file')
        fname_write = os.path.join(tmp_path, ('page_' + str(idx) + '.png'))

        # 1.直接元素截图
        # 获取页面截图并写入文件
        # png_body = driver.find_element_by_id('pagepb_' + str(idx))
        # png_body.screenshot(fname_write)
        # 2.窗口截图
        driver.get_screenshot_as_file(fname_write)
        # with open(fname_write, 'wb') as f_png:
        #     png_binary_data = driver.get_screenshot_as_png()
        #     # print(png_binary_data)
        #     write_size = f_png.write(png_binary_data)
        #     print('100% 大小为：' + str(write_size) + ' 字节')
        # 3.保存canvas
        # canvas = driver.find_element_by_id('outer_page_' + str(idx))
        # canvas = canvas.find_element_by_xpath('canvas')
        # canvas.screenshot(fname_write)
        png_list.append(fname_write)
        print('100%')

    # 退出页面
    driver.quit()

    return title, png_list


@time_cost(bconf['time_cost_type'])
def __make_pdf(fname, png_list):
    """
        __make_pdf
    :param fname:
    :param png_list:
    :return:
    """
    print('文件路径为：' + fname)
    img = Image.open(png_list[0])
    # print(img.size)
    pdf = canvas.Canvas(filename=fname, pagesize=img.size)  # 第一张图片的尺寸新建pdf

    for png in png_list:
        pdf.drawImage(png, 0, 0)
        pdf.showPage()
    pdf.save()


@time_cost(bconf['time_cost_type'])
def __rm_files(file_list):
    """
        __rm_files
    :param file_list:
    :return:
    """
    print('清理缓存')
    for file in file_list:
        os.remove(file)


@time_cost(bconf['time_cost_type'])
def doc88_pdf(url, fpath, fname=None):
    print('开始解析地址：' + url)

    if not os.path.exists(fpath):
        print('创建新目录：' + fpath)
        os.mkdir(fpath)

    # 获取文档的所有截图
    title, png_list = __get_png_list(url, fpath)
    if title and png_list:
        # 生成pdf文件
        if fname:
            __make_pdf(os.path.join(fpath, fname + '.pdf'), png_list)
        else:
            __make_pdf(os.path.join(fpath, title + '.pdf'), png_list)

    # 清理缓存文件
    __rm_files(png_list)
