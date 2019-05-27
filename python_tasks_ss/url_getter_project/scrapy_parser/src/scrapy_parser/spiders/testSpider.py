import scrapy
import json
from scrapy.selector import Selector
import sys
sys.path.append('/usr/home/itymos/git_thing/my-repo/python_tasks_ss/url_getter_project/scrapy_parser/src/scrapy_parser')
from scrapy_parser.items import TestItem
from scrapy.http import Request

class TestSpider(scrapy.Spider):
    name = 't_spider'
    custom_settings = {'ITEM_PIPELINES': {}, "LOG_LEVEL": "DEBUG",
            'FEED_FORMAT': 'csv', 'ITEM_PIPELINES': {}, "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36Edge/17.17134',
            'COOKIES_ENABLED': False, 'DOWNLOAD_DELAY': 1}
    # 30 per page

    def start_requests(self):
        req_list = [Request("https://www.yellowpages.com/austin-tx/plumbers")]
        return req_list

    def parse(self, response):
        res = response.css("div#main-content div.scrollable-pane div.organic \
div.result[id^='lid-'] div.srp-listing div.v-card div.info")
        pagination = response.css("div.pagination ul")
        for i in pagination:
            i.xpath("li")
        for i in res:
            if i.css("div.info-secondary div.links a.track-map-it").get():
                item = {'company_name': i.css("h2 a span::text").get(),
                        'address': ' '.join(i.css("div.info-primary p.adr span\
::text").getall()).replace('\xa0', ''), 'phone_number': ''.join(filter(lambda x:
                                                   x not in ['(', ')',' ', '-'],
                                                   i.css("div.info-primary \
div.phones::text").get(default='')
                                                   ))
                        }
                yield item

