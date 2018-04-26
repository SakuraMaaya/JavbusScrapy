# -*- coding: utf-8 -*-
import  scrapy
from scrapy.selector import Selector
from javbus.items import JavType

class JavSpider(scrapy.Spider):
    name = "javtypes"

    start_urls = ["https://www.javbus6.pw/genre"]

    custom_settings = {
        "ITEM_PIPELINES" : {
            "javbus.pipelines.JavTypePipeline" : 100
        }
    }
    def parse(self, response):
        orderNum = 1
        for parentType in response.xpath('.//h4[not(@*)]'):
            for type in parentType.xpath('following-sibling::div[1]/a'):
                item = JavType()
                item['topType'] = parentType.xpath('text()').extract()[0]
                item['name'] = type.xpath('text()').extract()[0]
                item['hash'] = orderNum
                orderNum += 1
                yield item
