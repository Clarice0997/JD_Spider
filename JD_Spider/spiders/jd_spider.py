import scrapy
from scrapy import Request
from JD_Spider.items import JdSpiderItem
import re
import json

class JdspiderSpider(scrapy.Spider):
    name = 'jd_spider'
    download_delay = 1
    allowed_domains = ['jd.com','3.cn']

    def __init__(self,GoodName):
        self.GoodName = GoodName

    # 自定义发起请求
    def start_requests(self):
        # 拼接搜索URL
        url = 'https://search.jd.com/Search?keyword='
        yield Request(url=url + self.GoodName, callback=self.parse)

    def parse(self, response):
        goods_list = response.xpath('//div[@id="J_goodsList"]/ul/li')
        # 遍历每一个商品
        for good in goods_list:
            item = JdSpiderItem()
            # 爬取商品标题
            title = good.xpath('div/div[@class="p-name p-name-type-2"]/a/em/text()').extract()
            Good_title = ''
            for name in title:
                Good_title = Good_title + ' ' +name
            # 去除前后空格
            Good_title = Good_title.strip()
            print(f"商品标题：{Good_title}")
            # 爬取商品店铺名
            Good_shopName = good.xpath('div/div[@class="p-shop"]/span/a/text()').extract_first()
            print(f"店铺名：{Good_shopName}")
            # 爬取商品id
            Good_id = good.xpath('@data-sku').extract_first()
            print(f"商品id：{Good_id}")
            # 爬取商品价格
            Good_price = good.xpath('div/div[@class="p-price"]/strong/i/text()').extract_first()
            print(f"商品价格：{Good_price}")
            # 爬取商品URL
            Good_url = response.urljoin(good.xpath('div/div[@class="p-name p-name-type-2"]/a/@href').extract()[0])
            print(f"商品URL：{Good_url}")
            # 构建item
            item['Good_title'] = Good_title
            item['Good_shopName'] = Good_shopName
            item['Good_id'] = Good_id
            item['Good_price'] = Good_price
            item['Good_url'] = Good_url
            # url创建请求 传递数据
            yield Request(url='http://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds='+Good_id, callback=self.parse_getCommentnum,meta={'item':item})

    def parse_getCommentnum(self,response):
        item1 = response.meta['item']
        # response.body是一个json格式的
        js = json.loads(str(response.body))
        Good_commentCount = js['CommentsCount'][0]['Score5Count']
        item1['Good_commentCount'] = Good_commentCount

        id = item1['Good_id']
        yield Request(url="https://item-soa.jd.com/getWareBusiness?callback=jQuery364464&skuId=" + id, callback=self.parse_intro, meta={'item': item1})


    def parse_intro(self,response):
        item = response.meta['item']
        temp = response.body.split('jQuery364464(')
        s = temp[:-1]  # 获取到需要的json内容
        js = json.loads(str(s))
        Good_brand = js['wareInfo.brandName']
        Good_name = js['wareInfo.wname']

        item['Good_brand'] = Good_brand
        item['Good_name'] = Good_name

        yield item

    def close(spider, reason):
        print("爬虫运行完毕")