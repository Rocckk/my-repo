# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
import pymysql
from .creds import USER, PASSWORD, DB


class UrlerMysqlPipeline(object):


    def open_spider(self, spider):
        print('$$$', object)
        self.connection = pymysql.connect(host='localhost', user=USER,
                                     password=PASSWORD, db=DB)

        webpage = spider.start_urls[0]
        webpage_count = self.check_presence(webpage)
        if webpage_count == 1:
            date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.insert_webpage(webpage, date, webpage_count)
        else:
            date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.update_webpage(webpage, date, webpage_count)

    def close_spider(self, spider):
        self.connection.close()
        print(30*'---')
        print('closed')


    def process_item(self, item, spider):
        webpage = spider.start_urls[0]
        self.insert_url(webpage, item['url'], item['count'])
        return item

    def insert_webpage(self, webpage, date, count):
        with self.connection.cursor() as cursor:
            if cursor.execute("insert into `webpages` (`url`, `time_crawled`,\
`crawl_count`) values ('{}', '{}', {})".format(webpage, date, str(count))):
                self.connection.commit()
            else:
                print('insertion failed!')

    def check_presence(self, url):
        with self.connection.cursor() as cursor:
            present = cursor.execute("select * from `webpages` where `url` =\
'{}'".format(url))
            if present:
                count = cursor.fetchone()
                return count[3] + 1
            return 1

    def update_webpage(self, webpage, date, count):
        with self.connection.cursor() as cursor:
            if cursor.execute("update `webpages` set `time_crawled` =\
'{}', `crawl_count` = {} where `url` = '{}'".format(date, count, webpage)):
                self.connection.commit()
            else:
                print('update failed')

    def insert_url(self, webpage, url, count):
        with self.connection.cursor() as cursor:
            if cursor.execute("insert into `scraped_urls` (`webpage_id`, `url`,\
`count_on_page`) values ((select `id` from `webpages` where `url` = '{}'), \
'{}', {})".format(webpage, url, str(count))):
                self.connection.commit()
            else:
                print('insertion url failed!')



