from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader
import re

def prepend_base_url_if_relative(url, loader_context):
    
    if url.startswith('/') and '://' not in url:
        base_url = loader_context.get('response').url
        return base_url + url
    return url

class BusinessProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    title_in = MapCompose(lambda x: x.replace("\n", "").replace("\xa0", "").strip())
    title_link_in = MapCompose(prepend_base_url_if_relative)
    Description_in = MapCompose(lambda x: x.replace("\n\t\t", "").replace("\xa0", "").replace("\"","").strip())
