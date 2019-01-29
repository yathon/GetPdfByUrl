# -*- coding:utf-8 -*-
__author__ = 'Yathon'
__time__ = '2018/12/14 10:46'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_chrome_driver(dpath=None):
    """
        get_chrome_driver
    :param dpath: chrome default download file path.
    :return: the chrome driver
    """
    chrome_options = webdriver.chrome.options.Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--window-size=2000,2700')
    if dpath:
        prefs = {'download.default_directory': dpath}
        chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path='./drivers/chrome/chromedriver', options=chrome_options)
    # driver.set_window_size(2000, 3000)
    if not driver:
        print('Get the chrome failed, please check the path.')
    return driver
