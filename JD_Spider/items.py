# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from itemadapter import ItemAdapter
import scrapy


class JdSpiderItem(scrapy.Item):
    GoodName = scrapy.Field()
    Good_id = scrapy.Field()
    Good_title = scrapy.Field()
    Good_price = scrapy.Field()
    Good_url = scrapy.Field()
    Good_brand = scrapy.Field()
    Good_shopName = scrapy.Field()
    Good_name = scrapy.Field()
    Good_commentCount = scrapy.Field()
    Good_comment = scrapy.Field()
