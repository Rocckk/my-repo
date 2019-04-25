"""
This module is a custom item pipeline which is used to interact with MySQL
database
"""
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
import pymysql
from .creds import USER, PASSWORD, DB


class UrlerMysqlPipeline(object):
    """
    This class implements a built-in scrapy item pipeline; it opens connection
    with a database, inserts into it the information about a scraped webpage
    and the URLs found on it and closes the connection
    """

    def open_spider(self, spider):
        """
        This method is called when the spider is opened; it opens a connection
        to a database, get the value of the webpage which is being scraped from
        a spider and call methods which write the info about the webpage to the
        database
        """
        self.connection = pymysql.connect(host='localhost', user=USER,
                                     password=PASSWORD, db=DB)
        self.webpage = spider.start_urls[0]
        self.handle_webpage(self.webpage)

    def close_spider(self, spider):
        """
        This method is called when the spider is closed; it closes the
        connection to a database
        """
        self.connection.close()


    def process_item(self, item, spider):
        """
        This method is called for every item pipeline component: every dict
        yielded by a spider;
        it checks how many times a single URL is encounted in a dabase and
        controls what to do with it next
        """
        count_present = self.check_presence_url(item['url'], self.webpage)
        if not count_present:
            self.insert_url(self.webpage, item['url'], item['count'])
        else:
            if count_present[0] != item['count']:
                self.update_url_count(count_present[1], item['url'],
                                      item['count'])
        return item

    def handle_webpage(self, webpage):
        """
        This is the custom method which is used to control what to do with the
        information on the webpage scraped: it checks if the webpage is already
        present in a database and if it is there already - updates the db,
        otherwise - create a new record in a db.
        params:
        webpage - str, the URL of the webpage which is being scraped
        """
        webpage_count = self.check_presence_webpage(webpage)
        if webpage_count == 1:
            date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.insert_webpage(webpage, date, webpage_count)
        else:
            date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.update_webpage(webpage, date, webpage_count)

    def insert_webpage(self, webpage, date, count):
        """
        This is the custom method which inserts a new record about a webpage
        scraped into a db
        params:
        webpage
        """
        with self.connection.cursor() as cursor:
            if cursor.execute("insert into `webpages` (`url`, `time_crawled`,\
`crawl_count`) values ('{}', '{}', {})".format(webpage, date, str(count))):
                self.connection.commit()
            else:
                print('insertion failed! for webpage {}'.format(webpage))

    def check_presence_webpage(self, url):
        """
        This is the custom method which checks if the scraped webpage is
        already in the database; if it is present - it increases its count and
        returns this count
        params:
        url - str, the URL of the webpage which is checked
        returns:
        1 - if there is not such webpage in a database (it will be the 1-st 
        insertion)
        otherwise - the count of webpage(the amount of times is was was scraped
        already increased by 1)
        """
        with self.connection.cursor() as cursor:
            present = cursor.execute("select * from `webpages` where `url` =\
'{}'".format(url))
            if present:
                record = cursor.fetchone()
                return record[3] + 1
            return 1

    def update_webpage(self, webpage, date, count):
        """
        This is the custom method which updates the information on the scraped
        webpage in the database
        params:
        webpage - str, the URL of the webpage which is checked
        date - str, the date when the webpage was scraped
        count - int, the number of times the webpage was scraped
        """
        with self.connection.cursor() as cursor:
            if cursor.execute("update `webpages` set `time_crawled` =\
'{}', `crawl_count` = {} where `url` = '{}'".format(date, count, webpage)):
                self.connection.commit()
            else:
                print('update failed for the webpage {}'.format(webpage))

    def check_presence_url(self, url, webpage):
        """
        This is the custom method which checks whether a URL which was found
        on the scraped webpage is already in tbe records in the db
        params:
        url - str, the URL which was found
        webpage - str, the webpage which has been scraped
        returns:
        False - if such URL is not in the db
        (count, webpage_id) - tuple, if such URL is already found in the db and
        it was scraped from the same wabpage;
        count - the amount of times it was found on the webpage
        webpage_id - the id of the webpage it was found on
        """
        with self.connection.cursor() as cursor:
            if cursor.execute("select `id` from `webpages` where `url` =\
'{}'".format(webpage)):
                webpage_id = cursor.fetchone()[0]
            present = cursor.execute("select `count_on_page` from \
`scraped_urls` where `url` = '{}' and `webpage_id` = {}".format(url, webpage_id))
            if present:
                count = cursor.fetchone()[0]
                return (count, webpage_id)
            return False

    def insert_url(self, webpage, url, count):
        """
        This is the custom method which inserts a new record about a certain
        URL which was found on the webpage scraped
        params:
        webpage, str, the URL of the webpage that has been scraped
        url - str, the URL which was found on the webpage
        count - int, the number of times the URL was encountered on the webpage
        """
        with self.connection.cursor() as cursor:
            if cursor.execute("insert into `scraped_urls` (`webpage_id`, `url`,\
`count_on_page`) values ((select `id` from `webpages` where `url` = '{}'), \
'{}', {})".format(webpage, url, str(count))):
                self.connection.commit()
            else:
                print('insertion of url failed for the URL {}!'.format(url))

    def update_url_count(self, webpage_id, url, count):
        """
        This is the custom method which updates the count of URLs found on the
        webpage in case this count changed
        params:
        webpage_id - int, the ID of the webpage on which the URL was found
        url - str, the URL which is updated
        count, int, the value which will replace the old count
        """
        with self.connection.cursor() as cursor:
            if cursor.execute("update `scraped_urls` set `count_on_page` =\
'{}' where `url` = '{}' and `webpage_id` = {}".format(count, url, str(webpage_id))):
                self.connection.commit()
            else:
                print('update of url {} failed'.format(url))



