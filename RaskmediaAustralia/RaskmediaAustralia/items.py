# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RaskmediaaustraliaItem(scrapy.Item):
    title = scrapy.Field()
    source_name = scrapy.Field()
    publisher_name = scrapy.Field()
    published_date = scrapy.Field()
    description = scrapy.Field()
