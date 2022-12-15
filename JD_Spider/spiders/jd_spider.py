import scrapy
from scrapy import Request

class JdspiderSpider(scrapy.Spider):
    name = 'jd_spider'
    download_delay = 3
    allowed_domains = ['www.jd.com']

    def __init__(self,GoodName):
        self.GoodName = GoodName

    # 自定义发起请求
    def start_requests(self):
        # 拼接搜索URL
        url = 'https://search.jd.com/Search?keyword='
        yield scrapy.Request(url=url + self.GoodName, callback=self.parse)

    def parse(self, response):
        pass

    def close(spider, reason):
        print("爬虫运行完毕")