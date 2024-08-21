# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# pipeline.py

import scrapy
import re
import pymongo
from itemadapter import ItemAdapter

class RemoveDuplicatesPipeline:
    def __init__(self):
        self.scraped_items = set()

    def process_item(self, item, spider):
        title = item['title']
        if title not in self.scraped_items:
            self.scraped_items.add(title)
            return item
        else:
            raise scrapy.exceptions.DropItem(f'Duplicate item found: {title}')




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
    rawdataBenzinga_collection = "rawdataBenzinga"
    refined_data4_collection = "Refined-data4"

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
            self.empty_collection(self.rawdataBenzinga_collection)  # Empty the collection if not already done
            self.empty_collection(self.refined_data4_collection)  # Empty the collection if not already done
        self.db[self.rawdataBenzinga_collection].insert_one(ItemAdapter(item).asdict())  # Insert new item into rawdataBenzinga
        self.db[self.refined_data4_collection].insert_one(ItemAdapter(item).asdict())  # Insert new item into Refined-data4
        return item