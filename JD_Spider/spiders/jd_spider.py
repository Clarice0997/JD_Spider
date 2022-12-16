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
            item['GoodName'] = self.GoodName
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
            yield Request(url="https://item-soa.jd.com/getWareBusiness?callback=jQuery364464&skuId=" + Good_id, callback=self.parse_intro, meta={'item': item}, dont_filter=True)

    def parse_intro(self,response):
        # 处理解析json
        item = response.meta['item']
        temp = response.text.split('jQuery364464(')[1][:-1]
        js = json.loads(temp,strict=False)
        # 爬取品牌名和商品型号
        Good_brand = js['wareInfo']['brandName']
        Good_name = js['wareInfo']['model']
        # 如果不存在商品型号，则使用标题
        if(Good_name == ''):
            Good_name = js['wareInfo']['wname']

        print(Good_brand)
        print(Good_name)

        item['Good_brand'] = Good_brand
        item['Good_name'] = Good_name

        # 存储item
        id = item['Good_id']
        url = f'https://sclub.jd.com/productpage/p-{id}-s-0-t-3-p-1.html'

        yield Request(url=url, callback=self.parse_comment, meta={'item': item},dont_filter=True)

    def parse_comment(self,response):
        # 处理解析json
        item = response.meta['item']
        js = json.loads(response.text,strict=False)
        comments = js['comments']
        Good_comment = ''
        # 爬取评论
        for comment in comments:
            print(comment['content'])
            Good_comment = Good_comment + comment['content'] + '/'
        print(Good_comment)
        # 爬取好评评价数
        Good_commentCount = js['productCommentSummary']['score5Count']

        print(Good_commentCount)
        print(Good_comment)

        # 存储item
        item['Good_commentCount'] = Good_commentCount
        item['Good_comment'] = Good_comment

        yield item

    def close(spider, reason):
        print("爬虫运行完毕")