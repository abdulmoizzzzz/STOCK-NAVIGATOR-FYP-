import scrapy

class BusinessinsiderusaItem(scrapy.Item):
    title = scrapy.Field()
    title_link = scrapy.Field()
    Description = scrapy.Field() 
    source_name = scrapy.Field()  # Define the Description field
    # published_by = scrapy.Field()
    # published_date = scrapy.Field()
