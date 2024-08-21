# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class MongoDBPipeline:
    rawdataAP_collection = "rawdataAP"
    Refined_data6_collection = "Refined-data6"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_empty = False  # Flag to track if collection is emptied

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
        self.db[collection_name].delete_many({})  # Empty the collection
        self.collection_empty = True  # Update flag to indicate collection is emptied

    def process_item(self, item, spider):
        if not self.collection_empty:  # Check if collection is already emptied
            self.empty_collection(self.rawdataAP_collection)  # Empty the collection if not already done
            self.empty_collection(self.Refined_data6_collection)  # Empty the collection if not already done
        self.db[self.rawdataAP_collection].insert_one(ItemAdapter(item).asdict())  # Insert new item into rawdataBusinessInsider
        self.db[self.Refined_data6_collection].insert_one(ItemAdapter(item).asdict())  # Insert new item into Refined-data5
        return item
