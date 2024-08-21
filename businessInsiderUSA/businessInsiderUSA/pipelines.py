# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import re

class CleanDescriptionPipeline:
    def process_item(self, item, spider):
        if 'Description' in item:
            # Remove \"
            item['Description'] = item['Description'].replace('\\"', '')
            # Remove leading and trailing whitespaces
            item['Description'] = item['Description'].strip()
            # Remove newline characters and extra whitespaces
            item['Description'] = re.sub(r'\s+', ' ', item['Description'])
        return item
    

class MongoDBPipeline:
    rawdataBusinessInsider_collection = "rawdataBusinessInsider"
    Refined_data5_collection = "Refined-data5"

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
            self.empty_collection(self.rawdataBusinessInsider_collection)  # Empty the collection if not already done
            self.empty_collection(self.Refined_data5_collection)  # Empty the collection if not already done
        self.db[self.rawdataBusinessInsider_collection].insert_one(ItemAdapter(item).asdict())  # Insert new item into rawdataBusinessInsider
        self.db[self.Refined_data5_collection].insert_one(ItemAdapter(item).asdict())  # Insert new item into Refined-data5
        return item