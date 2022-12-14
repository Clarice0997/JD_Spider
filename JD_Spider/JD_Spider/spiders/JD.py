import scrapy


class JdSpider(scrapy.Spider):
    name = 'JD'
    allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']

    def parse(self, response):
        pass
