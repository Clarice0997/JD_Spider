# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo

class JdMongodbPipeline:
    def open_spider(self, spider):
        self.conn = pymongo.MongoClient()
        self.db = self.conn['JD_shop']
        self.collection = self.db['JD_Goods']

    def process_item(self, item, spider):
        document = {
            '商品ID': item['Good_id'],
            '商品标题': item['Good_title'],
            '商品价格': item['Good_price'],
            '商品URL': item['Good_url'],
            '商品品牌': item['Good_brand'],
            '店铺名': item['Good_shopName'],
            '商品名称': item['Good_name'],
            '商品评论数': item['Good_commentCount'],
        }
        self.collection.update_one(document, {'$set': document}, upsert=True)
        return item

    def close_spider(self, spider):
        print('MongoDB存储完成')
        self.conn.close()


# class JdMongodbPipeline:
#     def open_spider(self, spider):
#         host = 'localhost'
#         port = 27017
#         db_name = 'JDShop'
#         self.client = pymongo.MongoClient(host=host, port=port)
#         self.db = self.client[db_name]
#         self.collection = self.db['Goods']
#         self.item_list = []
#
#     def process_item(self, item, spider):
#         self.item_list.append(dict(item))
#         return item
#
#     def close_spider(self, spider):
#         self.collection.insert_many(self.item_list)
#         print('{}条数据已存入数据库'.format(len(self.item_list)))
#         self.client.close()
#         print('数据库已关闭')
