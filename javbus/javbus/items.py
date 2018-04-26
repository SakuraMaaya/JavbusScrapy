# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JavbusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    thumb = scrapy.Field()
    thumb_url = scrapy.Field()
    thumb_path = scrapy.Field()

    cover = scrapy.Field()
    cover_url = scrapy.Field()
    cover_path = scrapy.Field()

    preview = scrapy.Field()
    preview_urls = scrapy.Field()
    preview_paths = scrapy.Field()

    title = scrapy.Field()
    artwork = scrapy.Field()
    bango = scrapy.Field()
    postTime = scrapy.Field()
    length = scrapy.Field()
    director = scrapy.Field()
    producer = scrapy.Field()
    series = scrapy.Field()
    types = scrapy.Field()
    actress = scrapy.Field()
    #演员id
    aid = scrapy.Field()
    magnets = scrapy.Field()
    link = scrapy.Field()

class JavType(scrapy.Item):
    #父类型
    topType = scrapy.Field()
    name = scrapy.Field()
    hash = scrapy.Field()