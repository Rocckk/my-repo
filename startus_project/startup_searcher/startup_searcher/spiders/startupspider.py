import json
import logging
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.exceptions import CloseSpider


class StartupSpider(scrapy.Spider):
	name = "startup_spider"

	def start_requests(self):
		req_list = [Request("https://e27.co/startups/load_startups_ajax?all&\
per_page={}&append=1".format(str(i))) for i in range(1, 28582)]
		return req_list

	def parse(self, response):
		startups_on_page = 16
		logging.info('started crawling {}'.format(response.url))
		page = json.loads(response.text)['pagecontent']
		names = Selector(text=page).css("h3.company-name::text").getall()
		request_urls = Selector(text=page).css("div.col-xs-12>a::attr(href)\
").getall()
		request_company_urls = Selector(text=page).xpath("//div[@class='desc']\
[contains(text(),'Website')]/following-sibling::div[@class='value'][1]")
		locations = Selector(text=page).css("div.col-xs-12:nth-child(2) \
div.value::text").getall()
		tags = Selector(text=page).css("div.col-xs-12:nth-child(3) div.value")
		logging.info('finished crawling {}'.format(response.url))
		if any([len(names) != startups_on_page,
				len(request_urls) != startups_on_page,
				len(request_company_urls) != startups_on_page,
				len(locations) != startups_on_page, len(tags) != startups_on_page
				]):
			logging.warning('the chosen selector did not find all the links \
which are on the page {}'.format(response.url))
			raise CloseSpider("not all the links were found on the page {}. The\
 selector has to be changed".format(response.url))
		for i in range(len(request_urls)):
			appendix = "?json"
			req = Request(request_urls[i] + appendix, callback=self.parse_pages)
			req.meta['name'] = names[i]
			req.meta['request_url'] = request_urls[i]
			req.meta['request_company_url'] = request_company_urls[i].css("a\
::attr(href)").get(default='')
			req.meta['location'] = locations[i].strip("\t\n")
			req.meta['tags'] = "; ".join(tags[i].css("a::text").getall())
			yield req

	def parse_pages(self, response):
		logging.info('started parsing {}'.format(response.url))
		founding_date = response.css("p span::text").get(default='')
		urls = response.css("div.socials a[target]::attr(href)").getall()
		short_description = response.css("div[style='font-size:16px;']::text\
").get(default='')
		description_long = Selector(response).css("p.profile-desc-text::text\
").getall()
		item = {'name': response.meta['name'],
				'request_url': response.meta['request_url'],
				'request_company_url': response.meta['request_company_url'],
				'location': response.meta['location'],
				'tags': response.meta['tags'], 'urls': "; ".join(urls),
				'founding_date': founding_date,
				'short_description': short_description,
				'description_long': ''.join(description_long).strip("\t\n")}
		logging.info('ended parsing {}'.format(response.url))
		yield item
