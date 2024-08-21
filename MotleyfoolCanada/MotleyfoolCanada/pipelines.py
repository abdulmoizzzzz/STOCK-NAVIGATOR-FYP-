# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class MongoDBPipeline:
    rawdatamotleycanada_collection = "rawdatamotleycanada"
    Refined_data10_collection = "Refined-data10"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_empty = False  

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def empty_collection(self, collection_name):
        self.db[collection_name].delete_many({})  
        self.collection_empty = True  

    def process_item(self, item, spider):
        if not self.collection_empty:  # Check if collection is already emptied
            self.empty_collection(self.rawdatamotleycanada_collection)  # Corrected collection name
            self.empty_collection(self.Refined_data10_collection)  # Corrected collection name
        self.db[self.rawdatamotleycanada_collection].insert_one(ItemAdapter(item).asdict())  # Insert new item into rawdatanewscom
        self.db[self.Refined_data10_collection].insert_one(ItemAdapter(item).asdict())  # Insert new item into Refined-data8
        return item
