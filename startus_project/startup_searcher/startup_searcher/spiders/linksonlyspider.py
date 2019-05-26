"""
This module contains the spider which scrapes the website https://e27.co/startups/
and collects the personal pages of all the startup companies listed there
"""
import json
import logging
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.exceptions import CloseSpider


class StartupSpider(scrapy.Spider):
	"""
	This is a the spider itself, which collects the personal pages of all the
	startup companies listed on https://e27.co/startups/;
	it accepts the optional input parameter 'num' which is the count of all the
	startups on https://e27.co/startups/;
	in order to write the results to the csv file the following command should
	be typed in terminal:
	scrapy crawl links_spider -o <filename.csv> [-a num=<number>]

	:param
	self.startup_num - int, the total number of startups, defaults to the most
	recent data: 28582
	self.per_page - int, as the page https://e27.co/startups/ is dynamically
	loaded and does not contain necessary data, the json-formatted pages like
	https://e27.co/startups/load_startups_ajax?all&per_page=1&append=1 are used
	to collect data; there are 16 items one every page, so this number comes
	from the observations
	self.num_of_pages - int, the number needed for the loop which generates the
	URLs which will be requested for data;
	"""
	name = "links_spider"

	def __init__(self, num=28582):
		super().__init__()
		self.startup_num = int(num)
		self.per_page = 16
		self.num_of_pages = self.startup_num // self.per_page + 1

	def start_requests(self):
		"""
		This method generates URLs which spider will send requests to
		:return:
		req_list, list, the list of Request objects
		"""
		req_list = [Request("https://e27.co/startups/load_startups_ajax?all&\
per_page={}&append=1".format(str(i)), meta={'num': i}) for i in
					range(1, self.num_of_pages + 1)]
		return req_list

	def parse(self, response):
		"""
		This method parses the response objects received and extracts necessary
		data; it closes the spider in case the selector did not find all the
		necessary data and logs the issue
		:param response: the response object for every URL
		"""
		logging.info('started scraping {}'.format(response.url))
		page = json.loads(response.text)['pagecontent']
		links = Selector(text=page).css("div.col-xs-12>a::attr(href)").getall()
		logging.info('finished scraping'.format(response.url))
		if len(links) == self.per_page:
			for i in range(len(links)):
				yield {'links': links[i]}
		elif response.meta['num'] == self.num_of_pages:
			for i in range(len(links)):
				yield {'links': links[i]}
		else:
			logging.warning('the chosen selector did not find all the links \
which are on the page {}'.format(response.url))
			raise CloseSpider("not all the links were found on the page {}. The\
 selector has to be changed".format(response.url))
