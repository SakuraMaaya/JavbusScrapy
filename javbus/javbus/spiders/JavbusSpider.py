# -*- coding: utf-8 -*-
import scrapy
import re
import time
from scrapy import Request
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor
from javbus.items import JavbusItem
from javbus import DataTools

class JavbusSpidr(scrapy.Spider):
    name = "javbus"

    start_urls = ["https://www.javbus6.pw/"]

    custom_settings = {
        'ITEM_PIPELINES' : {
            'javbus.pipelines.JavbusThumbPipeline': 10,
            'javbus.pipelines.JavbusCoverPipeline': 20,
            'javbus.pipelines.JavbusPreviewPipeline': 30,
            # "javbus.pipelines.JavTypePipeline" : 1,
            'javbus.pipelines.JavbusPipeline': 40,
        }
    }

    dataTool = DataTools.DataTools()
    homePage = "https://www.javbus6.pw/"

    #主页解析
    def parse(self, response):
        # self.logger.debug('In Home Parse')
        movies = response.xpath('//a[@class="movie-box"]')
        for movie in movies:
            detail_url = movie.xpath('@href').extract()[0]
            item = JavbusItem()
            item["thumb_url"] = movie.xpath('div[@class="photo-frame"]/img/@src')[0].extract()
            item["link"] = detail_url
            bango = detail_url.split('/')[-1]
            if not self.dataTool.is_crawled(bango):
                yield Request(url=detail_url, meta={'item':item}, callback=self.detail_prase,priority = 10)
            else:
                continue
            break
       # yield Request(url=self.next_page(response),callback=self.parse)

    #详情页解析
    def detail_prase(self, response):
        # self.logger.debug('IN Detail Parse')
        item = response.meta['item']

        item['title'] = response.xpath('//h3/text()').extract()[0]
        item['bango'] = response.xpath('//span[text()="識別碼:"]/parent::*/span[2]/text()').extract()[0]

        post = response.xpath('//span[text()="發行日期:"]/parent::*/text()').extract()[0].strip()
        item['postTime'] = time.strptime(post,'%Y-%m-%d')

        item['length'] = int(response.xpath('//span[text()="長度:"]/parent::*/text()').extract()[0].strip().replace('分鐘',''))
        director = response.xpath('//span[text()="導演:"]/parent::*/a/text()').extract()
        item['director'] = director[0] if len(director) > 0 else '无信息'

        item['producer'] = response.xpath('//span[text()="製作商:"]/parent::*/a/text()').extract()[0]
        item['artwork'] = response.xpath('//span[text()="發行商:"]/parent::*/a/text()').extract()[0]

        series = response.xpath('//span[text()="系列:"]/parent::*/a/text()').extract()
        item['series'] = series[0] if len(series) > 0 else ''

        item['cover_url'] = response.xpath('//img[@title]/@src').extract()[0]
        item['preview_urls'] = response.xpath('//a[@class="sample-box"]/@href').extract()

        types = []
        for type in response.xpath('//p[text()="類別:"]/following-sibling::p[1]/span/a/text()').extract():
            types.append(self.dataTool.get_type_id(type))
        item['types'] = types

        actress = []
        for actor in response.xpath('//span[@onmouseover]'):
            actress.append(actor.xpath('a/text()').extract_first())
        item['actress'] = actress

        headers = get_project_settings()['DEFAULT_REQUEST_HEADERS'].copy_to_dict()
        headers['referer'] = item["link"]

        yield Request(url=self.get_magnet_ajaxurl(response), meta={'item': item}, callback=self.get_magnet, headers=headers,priority = 20)

    def showLog(self,log):
        self.logger.debug(log)
    #拿磁力链请求地址
    def get_magnet_ajaxurl(self,response):
        parms = response.xpath("//script[contains(text(),'gid')]/text()").extract()[0].split(';')
        gid = re.search('\d+', parms[0]).group()
        uc = re.search('\d+', parms[1]).group()
        img = re.search("(?<=')[^']*", parms[2]).group()

        return self.homePage + ("ajax/uncledatoolsbyajax.php?gid=%s&img=%s&uc=%s"%(gid, img, uc))

    #拿磁力链
    def get_magnet(self,response):
        # self.logger.debug('In Magnet')
        item = response.meta['item']
        magnets = []
        for infos in response.xpath('//tr'):
            magnet = {'link':infos.xpath('td[1]/a/@href').extract_first()}
            info = infos.xpath('td')
            magnet['name'] = info[0].xpath('a[1]/text()').extract_first()
            magnet['size'] = info[1].xpath('a[1]/text()').extract_first()
            magnet['post_time'] = info[2].xpath('a[1]/text()').extract_first()
            magnets.append(magnet)
        item['magnets'] = magnets
        #结束
        # self.logger.info('\'' + item['link'] + '\' Crawl Info Over')
        yield item

    #拿下一页
    def next_page(self, response):
        nextPage = response.xpath('//a[@id="next"]/@href')
        if len(nextPage) > 0:
            nextPageurl = nextPage.extract()[0]
            nextPageurl = self.homePage + nextPageurl
            return nextPageurl
        return None
