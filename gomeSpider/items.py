# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Recruitment(scrapy.Item):
    id = scrapy.Field()
    job = scrapy.Field()
    sal = scrapy.Field()
    com = scrapy.Field()
    req = scrapy.Field()
    address = scrapy.Field()



class CYGItem(scrapy.Item):
    id = scrapy.Field()
    menpai = scrapy.Field()
    dengji = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    area = scrapy.Field()
    mainAttention = scrapy.Field()
    mainAttentionVal = scrapy.Field()
    jiankang = scrapy.Field()
    jianxiaxian = scrapy.Field()
    maindef = scrapy.Field()
    mainDefValue = scrapy.Field()
    HP = scrapy.Field()
    mingzhong = scrapy.Field()
    shanbi = scrapy.Field()
    chuanci = scrapy.Field()
    ccfy = scrapy.Field()
    shengdingTL = scrapy.Field()
    shendingAtt = scrapy.Field()
    price = scrapy.Field()
    zhuangbei = scrapy.Field()
    baoshi = scrapy.Field()
    xiunian = scrapy.Field()
    xinfa = scrapy.Field()
    leftTime = scrapy.Field()


class GomespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
