# -*- coding:utf-8 -*-
import scrapy
from scrapy import item
from scrapy import Selector
from scrapy.http import Request
from scrapy.http import Response
from gomeSpider.items import CYGItem
import MySQLdb
import sys
import time

class CYGSpider(scrapy.Spider):
    name = "CYGSELL"
    start_urls = ["http://tl.cyg.changyou.com/goods/public"] #http://tl.cyg.changyou.com/goods/selling  /goods/public
    reload(sys)
    sys.setdefaultencoding("utf8")

    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='123456', db='scrapy',charset='utf8')
    cursor = conn.cursor()



    def parse(self, response):
        self.parseSell(response)



    def parseSell(self,response):
        for result in response.xpath('//*[@class="order-list table-list"]/li'):
            url = result.xpath('a/@href').extract()[0]
            id = url.split("serial_num=")[1]
            price = result.xpath('span[1]/text()').extract()[0].split("¥")[1]
            time = result.xpath('span[2]/text()').extract()[0].split("成交")[0]
            self.saveSell(id, price, time)

    def saveSell(self,id,price,time):
        try:
            sql = "REPLACE INTO CYGSELL values('%s',%d,'%s')" %(id,int(price),time)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception, e:
            print str(e)











