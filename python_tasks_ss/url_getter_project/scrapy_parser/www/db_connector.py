"""This module is this Flask app's DB connector"""

import pymysql
import sys
import os
sys.path.append("/usr/home/itymos/git_thing/my-repo/python_tasks_ss/url_\
getter_project/scrapy_parser/")
from src.scrapy_parser.creds import USER, PASSWORD, DB
from src.scrapy_parser.logger import get_logger
import script_loader

class FlaskDbConnector:
    """
    This class is the database connector itself in a form of content manager;
    it checks the input source URL and checks the db for the links found on the
    source URL in case it has already been scraped before, otherwise - runs a
    shell script which launches the scrapy_parser project and scrapes the
    source URL, after that the links are looked for in the db
    params:
    self.host = str, the localhost be default, needed for the connection to the
    db
    self.logger - the custom logger used to log messages during the program
    execution
    self.source - str, the source URL which is checked against the db
    """
    def __init__(self, source=None, limit=None, offset=None, top=None):
        self.host = 'localhost'
        self.logger = get_logger()
        self.source = source
        self.limit = limit
        self.offset = offset
        self.top = top

    def __enter__(self):
        """
        This method opens a connection to the db and returns itself
        returns:
        self - the instance of the class itself
        """
        self.connection = pymysql.connect(host=self.host, user=USER,
                                          password=PASSWORD, db=DB)
        self.cursor = self.connection.cursor()
        self.logger.info("opened db connection by {}".format(str(os.getpid())))
        return self

    def handle_source(self):
        """
        This method checks is the source URl was provided, checks is the 
        source URL in the db already and gets links found on it;
        if the source URL is not in the db - it runs a script which scrapes
        URLs from it and returns them
        returns:
        links, list, the list of links found on the source URL;
        int - if nothing was found in the db, the number resembles the HTTP
        response status code
        """
        if self.source:
            self.trim_source()
            present = self.check_presence()
            if present:
                links = self.get_links(self.limit, self.offset)
                raw_links = self.get_links()
                if links:
                    total = self.get_total()
                    top, links_and_counts = self.get_top_links_counts(links,
                                                                      raw_links)
                    return (list(links_and_counts.items()), present, top,
                            total)
                else:
                    return 204
            elif script_loader.run(self.source):
                self.restart_conn()
                links = self.get_links(self.limit, self.offset)
                raw_links = self.get_links()
                if links:
                    total = self.get_total()
                    top, links_and_counts = self.get_top_links_counts(links,
                                                                      raw_links)
                    return (list(links_and_counts.items()), present, top,
                            total)
                else:
                    return 204
            self.logger.warning("the scrapy_parser script did not run well!")
            return 500
        self.logger.warning("the source URL was not provided to the DB \
connector")
        return 400

    def check_presence(self):
        """
        This method checks is the source URL is present in the db already
        returns:
        True, if yes
        False - if otherwise
        """
        present = self.cursor.execute("select * from `sources` where `url` =\
'{}'".format(self.source))
        if present:
            return True
        return False

    def get_links(self, limit=None, offset=None):
        """
        This method get the links found on the source URL from the db
        returns:
        links, list, the list of tuples containing links found in the db and 
        their count
        """
        if limit or offset:
            query = "select distinct `urls`.`url` from `urls` join `urls_to_\
sources` on `urls`.`id` = `urls_to_sources`.`url_id` join `sources` on \
`sources`.`id` = `urls_to_sources`.`source_id` where `sources`.`url` = '{}' \
order by `urls`.`url` limit {} offset {}".format(self.source, limit, offset)
        else:
            query = "select `urls`.`url` from `urls` join `urls_to_\
sources` on `urls`.`id` = `urls_to_sources`.`url_id` join `sources` on \
`sources`.`id` = `urls_to_sources`.`source_id` where `sources`.`url` = '{}'\
order by `urls`.`url`".format(self.source)
        if self.cursor.execute(query):
            links = []
            result = self.cursor.fetchall()
            for item in result:
                links.append(item[0])
            return links
        self.logger.info("no links were found in the db for the source URL {} \
because scraping on this page is likely forbidden by robots.txt file\
".format(self.source))

    def get_top_links_counts(self, links, raw_links):
        """
        This method finds out which links are found on the scraped web page the
        most times
        params:
        links - list of tuples: 1-st element - string, a link itself, 2-nd
        element - int, the number of times it's found on the webpage
        returns:
        top - the list of links found the most times
        """
        counts = {l: raw_links.count(l) for l in links}
        if self.cursor.execute("select `urls`.`url`, count(`urls_to_sources`.\
`url_id`) from `urls` join `urls_to_sources` on `urls`.`id` = `urls_to_sources`\
.`url_id` join `sources` on `sources`.`id` = `urls_to_sources`.`source_id` \
where `sources`.`url` = '{0}' group by `urls`.`url` having count(`urls_to_\
sources`.url_id) = (select count(urls_to_sources.url_id) from `urls` join \
`urls_to_sources` on `urls`.`id` = `urls_to_sources`.`url_id` join `sources` \
on `sources`.`id` = `urls_to_sources`.`source_id` where `sources`.`url` = '{0}'\
 group by `urls`.`url` order by count(urls_to_sources.url_id) desc limit 1)\
 ".format(self.source)):
            top_results = self.cursor.fetchall()
            top = {i[0]: i[1] for i in top_results}
            return (top, counts)

    def get_total(self):
        """
        This method calculates home many URL records associated with the source
        web page are there in the db
        returns:
        total_count - int, the number of URLs
        """
        if self.cursor.execute("select count(distinct `urls`.`url`) from `urls`\
 join `urls_to_sources` on `urls`.`id` = `urls_to_sources`.`url_id` join \
`sources` on `sources`.`id` = `urls_to_sources`.`source_id` where \
`sources`.`url` = '{}'".format(self.source)):
            total_count = self.cursor.fetchone()[0]
            return total_count

    def restart_conn(self):
        """
        This method closes and reopens the connection to the db to enable this
        context manager to get updated information, because unless the initial
        connection is used the context manager does not notice any changes to
        the db done by script_loader module
        """
        self.cursor.close()
        self.connection.close()
        self.connection = pymysql.connect(host=self.host, user=USER,
                                          password=PASSWORD, db=DB)
        self.cursor = self.connection.cursor()

    def trim_source(self):
        """
        This method trims the source URl provided to this DB connector to make
        sure the db lookups are correct: it removes trailing and leading spaces
        and forward slashes at the end from the source URL;
        """
        fragment_start = self.source.find("#")
        if fragment_start != -1:
            self.source = self.source[:fragment_start].strip(" /")
        else:
            self.source = self.source.strip(" /")

    def get_top_total(self):
        """
        This method checks what are the top 100, 50, 20, 10 URLs in the db;
        returns:
        result_list, list of tuples, containing the url, number of times it 
        was found totally and number of times it was found on each website;
        """
        if self.cursor.execute("select urls.id, urls.url, count(urls_to_sources\
.url_id) from urls join urls_to_sources on urls.id = urls_to_sources.url_id \
group by urls.url, urls.id order by count(urls_to_sources.url_id) desc, \
count(distinct(urls_to_sources.source_id)) desc limit {}".format(self.top)):
            result = self.cursor.fetchall()
            result_list = []
            for i in result:
                if self.cursor.execute("select sources.url, \
count(urls_to_sources.url_id) from sources join urls_to_sources on \
urls_to_sources.source_id = sources.id where urls_to_sources.url_id = {} group \
by sources.url;".format(i[0])):
                    occurences = self.cursor.fetchall()
                    result_list.append((i[1], i[2], occurences))
            return result_list

    def suggest_source(self):
        if self.cursor.execute("select `url` from `sources` where `url` like \
'{}%' order by `url`".format(self.source)):
            result = self.cursor.fetchall()
            result_list = [i[0] for i in result]
            return result_list

    def __exit__(self, type, value, traceback):
        """
        This method is the standard exit method of a context manager which
        closes all the available connections to the db
        """
        self.cursor.close()
        self.connection.close()
        self.logger.info("closed db connection")
