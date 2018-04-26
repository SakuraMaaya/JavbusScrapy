import codecs
import json
import os
import pymysql
import time
import logging

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class JavbusThumbPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(url = item['thumb_url'], meta = {'bango' : item['bango']})

    def file_path(self, request, response=None, info=None):
        bango = request.meta['bango']
        image_type = request.url.split('/')[-1].split('.')[-1]
        return '%s/%s.%s' %(bango, 'thumb',image_type)

    def item_completed(self, result, item, info):
        path = [x['path'] for ok, x in result if ok]

        item['thumb_path'] = path
        return item

class JavbusCoverPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(url = item['cover_url'], meta = {'bango' : item['bango']})

    def file_path(self, request, response=None, info=None):
        bango = request.meta['bango']
        image_type = request.url.split('/')[-1].split('.')[-1]
        return '%s/%s.%s' %(bango, 'cover',image_type)

    def item_completed(self, result, item, info):
        path = [x['path'] for ok, x in result if ok]
        item['cover_path'] = path
        return item

class JavbusPreviewPipeline(ImagesPipeline):
    preview = 0
    def get_media_requests(self, item, info):
        for preview in item['preview_urls']:
            self.preview += 1
            yield Request(url = preview, meta = {'bango' : item['bango']})

    def file_path(self, request, response=None, info=None):
        bango = request.meta['bango']
        image_type = request.url.split('/')[-1].split('-')[-1]
        return '%s/%s%s.%s' %(bango, 'preview', '_', image_type)

    def item_completed(self, result, item, info):
        path = [x['path'] for ok, x in result if ok]
        item['preview_paths'] = path
        return item

class JavbusPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='1234', db='Javbus', charset='utf8')
        self.cursor = self.conn.cursor()
        sql = '''
            CREATE TABLE IF NOT EXISTS MovieData(
              bango         VARCHAR(200) PRIMARY KEY,
              title         TEXT,
              artwork       VARCHAR(200),
              postTime      DATE,
              length        INTEGER,
              director      VARCHAR(200),
              producer      VARCHAR(200),
              series        VARCHAR(200),
              types         TEXT,
              link          VARCHAR(200),
              thumb_path    TEXT,
              cover_path    TEXT,
              preview_paths TEXT
            ) DEFAULT CHARSET=utf8;'''
        self.cursor.execute(sql)
        sql = '''
            CREATE TABLE IF NOT EXISTS ActressData(
              aid     VARCHAR(50) PRIMARY KEY,
              name    VARCHAR(200)
            ) DEFAULT CHARSET=utf8;'''
        self.cursor.execute(sql)
        sql = '''
            CREATE TABLE IF NOT EXISTS Magnets(
              magnet  VARCHAR(255) PRIMARY KEY,
              name    VARCHAR(200),
              size    INT
            ) DEFAULT CHARSET=utf8;'''
        self.conn.commit()

    def process_item(self, item, spider):
        sql = '''
            INSERT INTO MovieData VALUES (
              %s
            )'''%(self.get_item_all_info(item))
        self.cursor.execute(sql)
        self.conn.commit()

    def get_item_all_info(self, item):
        s = '''
        '%s',
        '%s',
        '%s',
        '%s',
        %s,
        '%s',
        '%s',
        '%s',
        '%s',
        '%s',
        '%s',
        '%s',
        '%s',
        '%s',
        '%s'
        '''%(
            item['bango'],
            item['title'],
            item['artwork'],
            time.strftime('%Y-%m-%d',item['postTime']),
            item['length'],
            item['director'],
            item['producer'],
            item['series'],
            json.dumps(item['types']),
            json.dumps(item['actress'],ensure_ascii=False),
            json.dumps(item['magnets'],ensure_ascii=False),
            item['link'],
            json.dumps(item['thumb_path'],ensure_ascii=False),
            json.dumps(item['cover_path'],ensure_ascii=False),
            json.dumps(item['preview_paths'],ensure_ascii=False),
        )
        return s

class JavTypePipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='1234', db='Javbus', charset='utf8')
        self.cursor = self.conn.cursor()

    def open_spider(self, spider):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TypeData(
              id      INT PRIMARY KEY,
              type    TINYTEXT,
              parent  TINYTEXT
            ) DEFAULT CHARSET=utf8;''')

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        sql = '''
            INSERT INTO TypeData(id, type, parent)
            VALUES (%s, "%s", "%s");
            ''' %(item['hash'], item['name'], item['topType'])
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print(sql)
            self.conn.rollback()
