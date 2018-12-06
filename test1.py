# -*- coding: utf-8 -*-
"""
使用Selenium模拟浏览器
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def main():
    # url = r'http://www.doc88.com/p-9005077529870.html'
    url = r'http://www.doc88.com/p-9119144870919.html'

    max_page = 7

    fpath = r'/Users/admin/Downloads/doc88/ZhouDeQingWeiShengWu/'
    # fname = r'part_1_page_'
    fname = r'part_2_page_'

    print('Init Chrome')
    time_all = time.time()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1250,1800')
    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    driver.set_window_size(1250, 1800)
    print('Init Chrome Cost:' + str(time.time() - time_all))

    print('Starting to get page')
    time_all = time.time()
    driver.get(url)

    fullscreen = driver.find_element_by_id('frscreen')
    fullscreen.click()

    bigger = driver.find_element_by_id('zoomInButton')
    time.sleep(0.6)
    bigger.click()
    time.sleep(0.6)
    bigger.click()
    time.sleep(0.6)
    bigger.click()
    time.sleep(0.6)
    bigger.click()

    page_num_input = driver.find_element_by_id('pageNumInput')
    print('get page Cost:' + str(time.time() - time_all))

    print('Starting to snap page')
    time_all = time.time()
    for idx in range(1, max_page):
        page_num_input.clear()
        page_num_input.send_keys(str(idx))
        page_num_input.send_keys(Keys.ENTER)

        for second in range(1, 40):
            time.sleep(1)
            print(second, end=' ')

        print('Write to file')
        time_start = time.time()
        fname_write = fpath + fname + str(idx) + '.png'
        with open(fname_write, 'wb') as f_png:
            write_size = f_png.write(driver.get_screenshot_as_png())
            print('File: ' + fname + str(idx) + '.png, size: ' + str(write_size))
        print('Write to file Cost:' + str(time.time() - time_start))

    print('Close driver')
    driver.quit()
    # driver.close()
    print('snap page Cost:' + str(time.time() - time_all))


if __name__ == '__main__':
    main()

