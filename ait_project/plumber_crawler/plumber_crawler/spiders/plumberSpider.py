import scrapy
from scrapy.http import Request

class PlumberSpider(scrapy.Spider):
    name = 'plumber_spider'
    # 30 per page

    def start_requests(self):
        req_list = [Request("https://www.yellowpages.com/austin-tx/plumbers")]
        return req_list

    def parse(self, response):
        print("entered", response.url)
        res = response.css("div#main-content div.scrollable-pane div.organic \
div.result[id^='lid-'] div.srp-listing div.v-card div.info")
        #pagination = response.css("div.pagination ul")
        # for i in pagination:
        #     i.xpath("li")
        for i in res:
            if i.css("div.info-secondary div.links a.track-map-it").get() or \
               i.css("div.links a.track-map-it").get():
                print("$$$", i.css("p.adr span::text").get(default='')) #  div,info-primary
                item = {'company_name': i.css("h2 a span::text").get(),
                        'address': ' '.join(i.css("p.adr span\
::text").getall()).replace('\xa0', ''), 'phone_number': int(''.join(filter(lambda x:
                                                   x not in ['(', ')',' ', '-'],
                                                   i.css("div.phones::text").get(default='0')
                                                   )))
                        }
                yield item
            else:
                print('failure', i.css("div.links").getall())
            next_page = response.xpath(
                "//div[@class='pagination']/ul/li[span]/following-sibling::li[1]/a/@href").get(
                default='')
            if next_page:
                print('##', next_page)
                next_page = response.urljoin(next_page)
                print('##', next_page)
                yield Request(next_page, callback=self.parse)

