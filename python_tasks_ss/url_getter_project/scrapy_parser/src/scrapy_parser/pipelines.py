"""
This module is a custom item pipeline which is used to interact with MySQL
database
"""
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from .creds import USER, PASSWORD, DB
from .logger import get_logger


class ScrapyParserMysqlPipeline:
    """
    This class implements a built-in scrapy item pipeline; it opens connection
    with a database, inserts into it the information about a scraped webpage
    and the URLs found on it and closes the connection
    """

    def open_spider(self, spider):
        """
        This method is called when the spider is opened; it opens a connection
        to a database, gets the value of the source which is being scraped from
        a spider and call methods which write the info about the source to the
        database; also it initiates a logger which will be used in a module
        """
        self.connection = pymysql.connect(host='localhost', user=USER,
                                          password=PASSWORD, db=DB)
        self.logger = get_logger()
        source = spider.start_urls[0]
        self.handle_source(source)

    def close_spider(self, spider):
        """
        This method is called when the spider is closed; it inserts a count of
        URLs which were encountered on the source web page and closes the
        connection to a database
        """
        self.insert_count()
        self.connection.close()

    def process_item(self, item, spider):
        """
        This method is called for every item pipeline component: every dict
        yielded by a spider;
        it checks how many times a single URL is encounted in a database and
        controls what to do with it next
        """
        present = self.check_presence_url(item['url'])
        if not present:
            self.insert_url(item['url'])
            self.insert_urls_sources(self.mod_source, item['url'])
        return item

    def handle_source(self, source):
        """
        This is the custom method which is used to control what to do with the
        information on the source web page scraped: it checks if the web page is
        already present in a database and if it is not there already - creates a
        new record in a db.
        params:
        source - str, the URL of the source web page which is being scraped
        """
        fragment_start = source.find("#")
        if fragment_start != -1:
            self.mod_source = source[:fragment_start].strip(" /")
        else:
            self.mod_source = source.strip(" /")
        present = self.check_presence_source(self.mod_source)
        if not present:
            self.insert_source(self.mod_source)

    def insert_source(self, source):
        """
        This is the custom method which inserts a new record about a source web
        page scraped into a db
        params:
        source - the URL of the source web page which has been scraped
        """
        with self.connection.cursor() as cursor:
            try:
                if cursor.execute("insert into `sources` (`url`) values ('{}')\
".format(source)):
                    self.connection.commit()
                else:
                    self.logger.warning('insertion failed! for source \
{}'.format(source))
            except pymysql.err.DataError:
                self.logger.warning('the source {} was not inserted due to \
problems with the data format'.format(source))

    def check_presence_source(self, url):
        """
        This is the custom method which checks if the scraped webpage is
        already in the database; if it is present - it returns True,
        otherwise - False
        params:
        url - str, the URL of the source web page which is checked
        returns:
        False - if there is not such web page in a database (it will be the 1-st
        insertion)
        otherwise - True
        """
        with self.connection.cursor() as cursor:
            present = cursor.execute("select * from `sources` where `url` =\
'{}'".format(url))
            if present:
                return True
            return False

    def insert_count(self):
        """
        This method checks how many URLs are encountered on a scraped source
        web page und updates the db with this number
        :param source: str, the URL of the source web page
        """
        try:
            with self.connection.cursor() as cursor:
                if cursor.execute("select count(`url_id`) from \
`urls_to_sources` where `source_id` = (select `id` from `sources` where `url` =\
'{}')".format(self.mod_source)):
                    count = cursor.fetchone()[0]
            with self.connection.cursor() as cursor:
                if cursor.execute("update `sources` set `count_of_urls` = {} \
where `url` = '{}'".format(count, self.mod_source)):
                    self.connection.commit()
        except pymysql.err.DataError:
            self.logger.warning('the source {} was not updated due to \
 problems with the data format'.format(self.mod_source))

    def check_presence_url(self, url):
        """
        This method checks if an URL is already inserted into a db or not
        :param url: str, the URL of the link found on the scraped web page
        :return:
        True - if such a URL has been found
        False - otherwise
        """
        with self.connection.cursor() as cursor:
            if cursor.execute("select * from `urls` where `url` =\
'{}'".format(url)):
                return True
            return False

    def insert_url(self, url):
        """
        This is the custom method which inserts a new record about a certain
        URL which was found on the web page scraped
        params:
        url - str, the URL which was found on the source web page
        """
        try:
            with self.connection.cursor() as cursor:
                if cursor.execute("insert into `urls` (`url`) values ('{}')\
".format(url)):
                    self.connection.commit()
                else:
                    self.logger.warning('insertion of url failed for the URL {}\
!'.format(url))
        except pymysql.err.DataError:
            self.logger.warning('the URL {} was not inserted due to \
problems with the data format'.format(url))

    def insert_urls_sources(self, source, url):
        """
        This is the custom method which insert new values it the table `urls_to_
        sources`
        :param source: str, the URL of the source web page which has been
        scraped
        :param url: str, the URL which was found on the source web page
        """
        try:
            with self.connection.cursor() as cursor:
                if cursor.execute("insert into `urls_to_sources` (`url_id`, \
        `source_id`) values ((select `id` from `urls` where `url` = '{}'), \
(select `id` from `sources` where `url` = '{}'))".format(url, source)):
                    self.connection.commit()
                else:
                    self.logger.warning('insertion into table `urls_to_sources`\
 failed for the URL {}!'.format(url))
        except pymysql.err.DataError:
            self.logger.warning('the URL {} was not inserted due to \
problems with the data format'.format(url))
