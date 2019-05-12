# -*- coding:utf-8 -*-

from scrapy import cmdline
import time
import os

def getSell():
    os.system("D:\\Python27\\python.exe D:/Python27/Lib/site-packages/scrapy/cmdline.py crawl CYG")

if __name__ == '__main__':
    while(True):
        print time.time()
        getSell()
        time.sleep(3600)