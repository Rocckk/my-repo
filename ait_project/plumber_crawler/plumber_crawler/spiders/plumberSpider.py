"""
This module implements a spider which looks for the plumbing services in Texas
according to the requirements
"""
import logging
import scrapy
from scrapy.http import Request

class PlumberSpider(scrapy.Spider):
    """
    This class is the spider itself, it scrapes all the necessary info
    recursively according to the requirements;
    it is already set up to save result data in json files, so it should be run
    like this:
    scrapy crawl plumber_spider -o <filename.json>
    """
    name = 'plumber_spider'

    def start_requests(self):
        req_list = [Request("https://www.yellowpages.com/austin-tx/plumbers")]
        return req_list

    def parse(self, response):
        logging.info('scraping started on {}'.format(response.url))
        res = response.css("div#main-content div.scrollable-pane div.organic \
div.result[id^='lid-'] div.srp-listing div.v-card div.info")
        for i in res:
            if i.css("div.info-secondary div.links a.track-map-it").get() or \
            i.css("div.links a.track-map-it").get():
                item = {'company_name': i.css("h2 a span::text").get(),
                        'address': ' '.join(i.css("p.adr span\
::text").getall()).replace('\xa0', ''),
                        'phone_number': int(''.join(filter(lambda x:
                                                           x not in ['(', ')',
                                                                     ' ', '-'],
                                                                     i.css("div.phones::text").get(default='0')
                                                          )
                                                    )
                                            )
                        }
                yield item
            else:
                continue
        next_page = response.xpath("//div[@class='pagination']/ul/li[span]\
/following-sibling::li[1]/a/@href").get(default='')
        if next_page:
            next_page = response.urljoin(next_page)
            logging.info('proceeding to the next page: {}'.format(next_page))
            yield Request(next_page, callback=self.parse)

