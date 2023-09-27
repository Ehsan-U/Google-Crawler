import scrapy
from urllib.parse import urlencode
from scrapy.crawler import CrawlerProcess
from scrapy import signals
import csv
import re


class GoogleBot(scrapy.Spider):
	name = "google_spider"


	def start_requests(self):
		for query in self.queries:
			params = urlencode({
				"q": query.get('query'),
				"num": 10,
				"hl": 'en',
				"start": 0,
			})
			url = "https://www.google.com/search?" + params
			yield scrapy.Request(url, callback=self.parse, meta={
				# "zyte_api": {
				# 	"httpResponseBody": True,
				# 	"httpResponseHeaders": True,
				# }
			})


	def parse(self, response, **kwargs):
		raw_text = " ".join(list(filter(None, map(lambda x: x if x.strip() else None, response.xpath("//div[@id='main']//text()[not(ancestor::script) and not(ancestor::style)]").getall()))))
		cleaned_text = re.sub(r"\s+", " ", raw_text).strip()
		item = {
			"query": response.xpath("//textarea[@aria-label='Search']/text()").get(),
			"text": cleaned_text
		}
		yield item


	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(GoogleBot, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
		return spider


	def spider_opened(self, spider):
		self.queries = []
		with open("queries.csv", 'r') as f:
			reader = csv.reader(f)
			next(reader)
			for idx, row in enumerate(reader, start=100):
				self.queries.append({
					"id": row[0],
					"query": row[1]
				})
				if idx == 500:
					break




# crawler = CrawlerProcess(settings={
# 		"CONCURRENT_REQUESTS": 8,
# 		"DOWNLOAD_DELAY": 3,
# 		"FEEDS": {"data.json": {"format":"json"}}
# 	})
# crawler.crawl(GoogleBot)
# crawler.start()