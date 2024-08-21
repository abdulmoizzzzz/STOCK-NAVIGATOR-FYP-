# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BenzingaprousaItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    title_link = scrapy.Field()
    published_date = scrapy.Field()
    publisher_name = scrapy.Field()
    Description = scrapy.Field()
    source_name = scrapy.Field()
   
