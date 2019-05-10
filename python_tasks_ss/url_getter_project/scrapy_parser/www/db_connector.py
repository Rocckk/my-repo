"""This module is this Flask app's DB connector"""

import pymysql
import sys
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
    def __init__(self, source):
        self.host = 'localhost'
        self.logger = get_logger()
        self.source = source

    def __enter__(self):
        """
        This method checks is the source URl was provided, opens a connection
        to the db, checks is the source URL in the db already and gets links
        found on it;
        if the source URL is not in the db - it runs a script which scrapes
        URLs from it and returns them
        returns:
        links, list, the list of links found on the source URL;
        int - if nothing was found in the db, the number resembles the HTTP
        response status code
        """
        self.connection = pymysql.connect(host=self.host, user=USER,
                                          password=PASSWORD, db=DB)
        self.cursor = self.connection.cursor()
        if self.source:
            self.trim_source()
            present = self.check_presence()
            if present:
                links = self.get_links()
                if links:
                    return links
                else:
                    return 204
            elif script_loader.run(self.source):
                self.restart_conn()
                links = self.get_links()
                if links:
                    return links
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

    def get_links(self):
        """
        This method get the links found on the source URL from the db
        returns:
        links, list, the list of links found in the db
        """
        if self.cursor.execute("select `urls`.`url` from `urls` join `urls_to_\
sources` on `urls`.`id` = `urls_to_sources`.`url_id` join `sources` on \
`sources`.`id` = `urls_to_sources`.`source_id` where `sources`.`url` = '{}'\
".format(self.source)):
            links = []
            result = self.cursor.fetchall()
            for item in result:
                links.append(item[0])
            return links
        self.logger.info("no links were found in the db for the source URL {}\
because scraping on this page is likely forbidden by robots.txt file\
".format(self.source))

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

    def __exit__(self, type, value, traceback):
        """
        This method is the standard exit method of a context manager which
        closes all the available connections to the db
        """
        self.cursor.close()
        self.connection.close()
        self.logger.info("closed db connection")
