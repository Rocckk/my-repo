"""this module is this Flask app's DB connector"""    

import pymysql
try:
    from scrapy_parser.creds import USER, PASSWORD, DB
    from scrapy_parser.logger import get_logger
except ModuleNotFoundError:
    import sys
    sys.path.append("/usr/home/itymos/git_thing/my-repo/python_tasks_ss/url_getter_project/scrapy_parser/src/")
    from scrapy_parser.creds import USER, PASSWORD, DB
    from scrapy_parser.logger import get_logger

class FlaskDbConnector:
    def __init__(self, source):
        self.connection = pymysql.connect(host='localhost', user=USER,
                                      password=PASSWORD, db=DB)
        self.logger = get_logger()
        self.source = source
        self.cursor = self.connection.cursor()

    def __enter__(self):
        present = self.check_presence()
        print('!!!', present)
        if present:
            links = self.get_links()
            return links
        return

    def check_presence(self):
        present = self.cursor.execute("select * from `sources` where `url` =\
'{}'".format(self.source))
        if present:
            return True
        return False

    def get_links(self):
        if self.cursor.execute("select `urls`.`url` from `urls` join `urls_to_sources`\
on `urls`.`id` = `urls_to_sources`.`url_id` join `sources` on `sources`.`id` = \
`urls_to_sources`.`source_id` where `sources`.`url` = '{}'\
".format(self.source)):
            links = []
            result = self.cursor.fetchall()
            for item in result:
                links.append(item[0])
            return links

            

    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.connection.close()
        print("closed")

