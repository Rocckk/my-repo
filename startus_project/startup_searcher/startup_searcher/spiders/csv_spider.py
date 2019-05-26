"""
This module implements a spider which reads the links from a csv file, and
searches for necessary information on them
"""
import logging
import scrapy
from scrapy.http import Request
from csv import DictReader


class StartupSpider(scrapy.Spider):
	"""
	This class is the spider itself which reads input data (links)
	from a csv file, and looks for the necessary information on every link
	:param
	self.filepath - str, the path to the file with the input links
	"""
	name = "csv_spider"

	def __init__(self, filepath):
		super().__init__()
		self.filepath = filepath

	def start_requests(self):
		"""
		This method reads the input csv file and create a list of requests from
		this file; it also handles exception if the path to the file is
		incorrect
		:return:
		req_list, list, the list of Request objects, if the file was not found -
		empty list
		"""
		req_list = []
		try:
			with open(self.filepath) as f:
				for row in DictReader(f):
					appendix = "?json"
					req_list.append(Request(row['links'] + appendix))
			return req_list
		except FileNotFoundError:
			logging.error("the file path provided to the spider is not correct:\
 the file {} cannot be found".format(self.filepath))
			return []

	def parse(self, response):
		"""
		This method parses response onbjects and scrapes the necessary
		information which is yielded
		:param response: the response object
		"""
		logging.info('started scraping {}'.format(response.url))
		name = response.css("h1.profile-startup::text").get(default='')
		request_url = response.url.replace('?json', '')
		request_company_url = response.css("span a[target]::attr(href)\
").get(default='')
		location = response.css("span a[href*='loc[]']::text").get(default='')
		tags = response.css("div[style^='word-wrap'] span a[href*='market']\
::text").getall()
		founding_date = response.css("p span::text").get(default='')
		urls = response.css("div.socials a[target]::attr(href)").getall()
		short_description = response.css("div[style='font-size:16px;']\
::text").get(default='')
		description_long = response.css('p.profile-desc-text::text').getall()
		founder = response.css("span.item-label a::text").get() if 'founder' \
				  in response.css("span.item-label+span.profile-desc-text\
::text").get(default='') else ''
		employee_range = len(response.css("div[id^='member']").getall())
		item = {'name': name, 'request_url': request_url,
				'request_company_url': request_company_url,
				'location': location, 'tags': "; ".join(tags),
				'urls': "; ".join(urls), 'founding_date': founding_date,
				'founders': founder, 'employee_range': employee_range,
				'email': '', 'phone': '', 'short_description': short_description,
				'description_long': ''.join(description_long).strip("\t\n")}
		logging.info('finished scraping'.format(response.url))
		yield item
