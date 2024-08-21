# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SimplywallgermanyItem(scrapy.Item):
    title = scrapy.Field()
    title_link = scrapy.Field()
    published_date = scrapy.Field()
    Description = scrapy.Field()
    source_name = scrapy.Field()
