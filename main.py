# -*- coding:utf-8 -*-

from doc88 import doc88_pdf as get_pdf, config


def main():
    url = r'http://www.doc88.com/p-9005077529870.html'
    # url = r'http://www.doc88.com/p-9119144870919.html'
    fpath = r'/Users/admin/Downloads/doc88/'

    for cnt in range(1, config.RETRY_CNT + 1):
        try:
            get_pdf(url, fpath)
            break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(ex)