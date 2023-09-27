import scrapy
from urllib.parse import urlencode
from scrapy.crawler import CrawlerProcess
from scrapy import signals
import csv


class QuoteBot(scrapy.Spider):
    name = "quotes_spider"

    def start_requests(self):
        for page in range(6, 10):
            url = f"https://books.toscrape.com/catalogue/page-{page}.html"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        products = response.xpath("//article/h3/a/@href").getall()
        yield from response.follow_all(urls=products, callback=self.parse_product)


    def parse_product(self, response):
        return {
            "Title": response.xpath("//title/text()").get()
        }






# crawler = CrawlerProcess(settings={
# 		"CONCURRENT_REQUESTS": 8,
# 		"DOWNLOAD_DELAY": 3,
# 		"FEEDS": {"data.json": {"format":"json"}}
# 	})
# crawler.crawl(GoogleBot)
# crawler.start()