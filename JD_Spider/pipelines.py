# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo

class JdMongodbPipeline:
    def open_spider(self, spider):
        host = 'localhost'
        port = 27017
        db_name = 'JDShop'
        # 连接MongoDB数据库
        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client[db_name]
        self.collection = self.db['Goods']
        # 暂存列表
        self.item_list = []

    def process_item(self, item, spider):
        # 暂存列表
        self.item_list.append(dict(item))
        print('process_item')
        return item

    def close_spider(self, spider):
        # MongoDB插入暂存列表
        self.collection.insert_many(self.item_list)
        print('{}条数据已存入数据库'.format(len(self.item_list)))
        self.client.close()
        print('MongoDB数据库已关闭')
