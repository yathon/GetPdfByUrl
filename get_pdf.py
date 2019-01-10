# -*- coding: utf-8 -*-

import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def main():
    url = r'http://www.doc88.com/p-9005077529870.html'
    # url = r'http://www.doc88.com/p-9119144870919.html'

    fpath = r'/Users/admin/Downloads/doc88/'

    print('Init Chrome')
    time_all = time.time()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=2000,2700')
    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    # driver.set_window_size(2000, 3000)
    print('Init Chrome Cost:' + str(time.time() - time_all))

    print('Starting to get page')
    driver.get(url)
    print('Starting to analyse page')

    # 获取文档标题并转义非法字符后作为文件名
    forbid_char = ' `~!@#$%^&*()+}{|":?><[]\\;\'/.,·～！@#¥%……&*（）——+-=「」|【】、；：/。，？》《'
    fname = driver.find_element_by_class_name('doctopic')
    fname = fname.find_element_by_xpath('h1').text
    # print('文档标题[' + fname + ']')
    for fchar in forbid_char:
        fname = fname.replace(fchar, '_')
    print('文件名[' + fname + ']')
    fpath = os.path.join(fpath, fname)
    if not os.path.exists(fpath):
        os.mkdir(fpath)

    # 获取最大页数
    max_page = int(driver.find_element_by_class_name('text').text[2:])
    print('文档页数[' + str(max_page) + ']')

    # 隐藏最上边条
    js = 'document.getElementsByClassName(\'header\')[0].style.display="none";'
    driver.execute_script(js)

    # 隐藏右上角提示
    js = 'document.getElementsByClassName(\'skintips\')[0].style.display="none";'
    driver.execute_script(js)

    # 隐藏右下角图标集
    js = 'document.getElementsByClassName(\'toplayer-shop\')[0].style.display="none";'
    driver.execute_script(js)

    # 页面全屏
    fullscreen = driver.find_element_by_id('frscreen')
    fullscreen.click()

    # 放大页面（点击放大按钮）
    bigger = driver.find_element_by_id('zoomInButton')
    for cnt in range(1, 4):
        bigger.click()
        time.sleep(0.3)

    # 获取跳转页面输入框句柄
    page_num_input = driver.find_element_by_id('pageNumInput')

    print('Starting to snap page')
    time_all = time.time()
    for idx in range(1, max_page):
        # 显示工具选项栏
        js = 'document.getElementsByClassName(\'readshop\')[0].style.display="block";'
        driver.execute_script(js)

        # 清空并输入需要跳转的页面后触发跳转
        page_num_input.clear()
        page_num_input.send_keys(str(idx))
        page_num_input.send_keys(Keys.ENTER)

        # 隐藏工具选项栏
        js = 'document.getElementsByClassName(\'readshop\')[0].style.display="none";'
        driver.execute_script(js)

        # 等待页面加载完成
        print('Waiting page [' + str(idx) + '] loading ...')
        for second in range(1, 300):
            load_percent = driver.find_element_by_id('pagepb_' + str(idx)).text
            if load_percent:
                time.sleep(1)
                print(load_percent, end=' ')
            else:
                break
        else:
            print('page [' + str(idx) + '] load timeout')
            print('Close driver')
            driver.quit()
            print('snap page Cost:' + str(time.time() - time_all))
            return
        print('\nWaiting page [' + str(idx) + '] loaded')

        print('Write to file')
        fname_write = fpath + '/page_' + str(idx) + '.png'
        # 1.直接元素截图
        # 获取页面截图并写入文件
        # png_body = driver.find_element_by_id('pagepb_' + str(idx))
        # png_body.screenshot(fname_write)
        # 2.窗口截图
        with open(fname_write, 'wb') as f_png:
            # 获取窗口截图并写入文件
            write_size = f_png.write(driver.get_screenshot_as_png())
            print('File: page_' + str(idx) + '.png, size: ' + str(write_size))
        # 3.保存canvas
        # canvas = driver.find_element_by_id('outer_page_' + str(idx))
        # canvas = canvas.find_element_by_xpath('canvas')
        # canvas.screenshot(fname_write)
        print('Write to file OK')

    # 退出页面
    print('Close driver')
    driver.quit()
    print('snap page Cost:' + str(time.time() - time_all))


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(ex)
