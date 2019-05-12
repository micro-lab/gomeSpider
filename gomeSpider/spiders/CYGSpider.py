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
    name = "CYG"
    #http://tl.cyg.changyou.com/goods/selling?world_id=0&order_by=remaintime-desc&have_chosen=&page_num=1#goodsTag
    #http://tl.cyg.changyou.com/goods/public?world_id=0&order_by=remaintime-desc&have_chosen=&page_num=1#goodsTag
    start_urls = ["http://tl.cyg.changyou.com/goods/selling?world_id=0&order_by=remaintime-desc&have_chosen=&page_num=1#goodsTag"] #http://tl.cyg.changyou.com/goods/selling  /goods/public
    reload(sys)
    sys.setdefaultencoding("utf8")

    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='123456', db='scrapy',charset='utf8')
    cursor = conn.cursor()



    def parse(self, response):
        for result in response.xpath('//*[@id="J_good_list"]/li'):
            name = result.xpath('dl/dt/a/text()').extract()[0]
            names = result.xpath('dl/dt/a/span/text()').extract()[0].split(" ")
            menpai = names[0].replace("[","")
            sex = "0"
            if(names[1] == "女"):
                sex = "1"
            dengji = names[2].replace("]","").replace("级","")
            url = result.xpath('dl/dt/a/@href').extract()[0]
            id = url.split("serial_num=")[1]
            # area = result.xpath('dl/dd[2]/span/text()').extract()[0]
            price = result.xpath('div/p[1]/text()').extract()[0].split("￥")[1]
            zhuangbei = result.xpath('dl/dd[1]/span[1]/b/text()').extract()[0]
            xiunian = result.xpath('dl/dd[1]/span[2]/b/text()').extract()[0]
            xinfa = result.xpath('dl/dd[1]/span[3]/b/text()').extract()[0]
            leftTime = result.xpath('//*[@id="J_good_list"]/li[1]/dl/dd[2]/p/text()').extract()[0].split("剩余时间：")[1]
            # print id,name,menpai,sex,dengji,price,area,xiunian,xinfa,leftTime
        #
        #
            rItem = CYGItem()
            rItem['id'] = id
            rItem['menpai'] = menpai
            rItem['dengji'] = dengji
            rItem['name'] = name
            rItem['sex'] = sex
            # rItem['area'] = area
            rItem['price'] = price
            rItem['zhuangbei'] = zhuangbei
            rItem['xiunian'] = xiunian
            rItem['xinfa'] = xinfa
            rItem['leftTime'] = leftTime

            if(self.exists(id)):
                continue

            yield Request(url, callback=self.parse_item,  meta = {'item' : rItem})
            time.sleep(3)

        next_page_url = response.xpath('//div[@class="ui-pagination"]/a[last()]/@href').extract()
        if next_page_url[0] != 'javascript:void(0)':
            yield scrapy.Request(next_page_url[0], callback=self.parse)



    def parse_item(self, response):
        item = response.meta['item']
        data = []
        bing = self.getAttentionPropertity('//*[@id="bing"]/div[2]/div/p',response)
        huo = self.getAttentionPropertity('//*[@id="huo"]/div[2]/div/p', response)
        xuan = self.getAttentionPropertity('//*[@id="xuan"]/div[2]/div/p', response)
        du = self.getAttentionPropertity('//*[@id="du"]/div[2]/div/p', response)
        #int(x [,base ])
        mainAttentionVal = str(max(int(bing[0]),int(huo[0]),int(xuan[0]),int(du[0])))
        if(mainAttentionVal==bing[0]):
            mainAttention = "1"
            jiankang = bing[2]
            jianxiaxian = bing[3]
        elif(mainAttentionVal==huo[0]):
            mainAttention = "2"
            jiankang = huo[2]
            jianxiaxian = huo[3]
        elif(mainAttentionVal == xuan[0]):
            mainAttention = "3"
            jiankang = xuan[2]
            jianxiaxian = xuan[3]
        elif(mainAttentionVal == du[0]):
            mainAttention = "4"
            jiankang = du[2]
            jianxiaxian = du[3]
        # print item['menpai'], bing[0], huo[0], xuan[0], du[0],mainAttention,mainAttentionVal,jiankang,jianxiaxian

        mainDefValue = str(max(int(bing[1]), int(huo[1]), int(xuan[1]), int(du[1])))
        if (mainDefValue == bing[1]):
            maindef = "1"
        elif (mainDefValue == huo[1]):
            maindef = "2"
        elif (mainDefValue == xuan[1]):
            maindef = "3"
        elif (mainDefValue == du[1]):
            maindef = "4"

        HP = response.xpath('//*[@id="goods-detail"]/div/div[2]/div/div[3]/span/i/text()').extract()[0]
        mingzhong = response.xpath('//*[@id="goods-detail"]/div/div[2]/div/div[15]/span/text()').extract()[0]
        shanbi = response.xpath('//*[@id="goods-detail"]/div/div[2]/div/div[16]/span/text()').extract()[0]
        chuanci = response.xpath('//*[@id="sword"]/div[2]/div/p/text()').extract()[0].split("：")[1]
        ccfy = response.xpath('//*[@id="shield"]/div[2]/div/p/text()').extract()[0].split("：")[1]
        shengdingTL = response.xpath('//*[@id="stove"]/div[2]/div/p[2]/text()').extract()[0].split("+")[1].strip()
        baoshi = response.xpath('//*[@id="goods-detail"]/div/div[4]/div[1]/div/div[6]/span/text()').extract()[0]
        area = response.xpath('//*[@class="server-info J-message"]/text()').extract()[0].replace(" ","").replace("所在区服：","").replace("\n","")

        # attData = []
        # print "=================================================================="
        # file_object = open('e:\\' + item['id'] + '.html', 'w')
        # file_object.write(response.body)
        # file_object.close()
        # for att in response.xpath('//ul[@class="row2 spirit"]/li'):
        #     print "--------------------------"
        #     va = att.xpath('span/text()').extract()[0]
        #     print va
        #     attData.append(va)
        # print "=================================================================="
        # shendingAtt = max(attData[0],attData[1],attData[2],attData[3])
        shendingAtt = "0"

        item['mainAttention'] = mainAttention
        item['mainAttentionVal'] = mainAttentionVal
        item['jiankang'] = jiankang
        item['jianxiaxian'] = jianxiaxian
        item['maindef'] = maindef
        item['mainDefValue'] = mainDefValue
        item['HP'] = HP
        item['mingzhong'] = mingzhong
        item['shanbi'] = shanbi
        item['chuanci'] = chuanci
        item['ccfy'] = ccfy
        item['shengdingTL'] = shengdingTL
        item['baoshi'] = baoshi
        item['shendingAtt'] = shendingAtt
        item['area'] = area

        try:
            sql = "REPLACE INTO CYGINFO values(" + item['id'] + ",'" + item['menpai'] + "'," + item['dengji'] + ",'" + \
                  item['name'] + "'," + item['sex'] + ",'" + item['area'] + "'," + item['mainAttention'] + "," + \
                  item['mainAttentionVal'] + "," + item['jiankang'] + "," + item[
                      'jianxiaxian'] + "," + item[
                      'maindef'] + "," + item['mainDefValue'] + "," + item['HP'] + "," + item['mingzhong'] + "," + item[
                      'shanbi'] + "," + item['chuanci'] + "," + item['ccfy'] + "," + item['shengdingTL'] + "," + item[
                      'shendingAtt'] + "," + item[
                      'price'] + "," + item[
                      'zhuangbei'] + "," + item[
                      'baoshi'] + "," + item[
                      'xiunian'] + "," + item[
                      'xinfa'] + ",'" + item[
                      'leftTime'] + "')"
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception, e:
            print str(e)


    def getAttentionPropertity(self,pathx,responsex):
        data = []
        for property in responsex.xpath(pathx):
            val = property.xpath('text()').extract()[0].split("+")[1].split(" ")[0]
            data.append(val)
        return data

    def exists(self, id):
        count = self.cursor.execute("select 1 from CYGINFO where id ="+id)
        if(count == 1):
            return True
        return False






