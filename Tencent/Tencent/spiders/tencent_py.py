# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem


class TencentPySpider(scrapy.Spider):
    name = 'tencent'
    # allowed_domains = ['tencent.com']
    base_url = "https://hr.tencent.com/position.php?lid=&tid=&keywords=请输入关键词&start="
    temp = 0
    url = base_url + str(temp)
    start_urls = [url]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for node in node_list:
            item = TencentItem()
            item['positionName'] = node.xpath("./td[1]/a/text()").extract()[0].encode("utf-8")
            item['positionLink'] = node.xpath("./td[1]/a/@href").extract()[0].encode("utf-8")
            # 爬去的网页中可能为空。做一个判断，防止代码报错
            if len(node.xpath("./td[2]/text()")):
                item['positionType'] = node.xpath("./td[2]/text()").extract()[0].encode("utf-8")
            else:
                item['positionType'] = ""

            item['positionNum'] = node.xpath("./td[3]/text()").extract()[0].encode("utf-8")
            item['positionAddress'] = node.xpath("./td[4]/text()").extract()[0].encode("utf-8")
            item['positionTime'] = node.xpath("./td[5]/text()").extract()[0].encode("utf-8")
            # 类比于return yield返回给管道
            yield item

        if self.temp < 3000:
            self.temp += 10
            # 自己定义的新的url
            newurl = self.base_url + str(self.temp)
            # 构建并发送请求 request两个参数
            yield scrapy.Request(newurl, callback=self.parse)