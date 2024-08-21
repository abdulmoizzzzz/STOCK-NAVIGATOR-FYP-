import scrapy
from StockHouseCanada.items import StockhousecanadaItem
import re

class StockhouseSpiderSpider(scrapy.Spider):
    name = "stockhouse_spider"
    allowed_domains = ["stockhouse.com"]
    start_urls = ["https://stockhouse.com/news/newswire"]
    source_name = "Stockhouse Canada"
    item_count = 0

    def parse(self, response):
        news = response.css('.hub-article-container')
        for new in news:
            item = StockhousecanadaItem()
            item['source_name'] = self.source_name  
            item['title'] = new.css('.clearfix.hub-article-container > h3 > a::text').get()
            item['title_link'] = new.css('.clearfix.hub-article-container > h3 > a::attr(href)').get()
            item['author'] = new.css('.clearfix.hub-article-container > div > a::text').get()
            
           
            yield scrapy.Request(item['title_link'], callback=self.parse_description, meta={'item': item})
            
            self.item_count += 1
            if self.item_count >= 100:
                self.logger.info("Scraped 100 items. Stopping spider.")
                return
            
        # Pagination logic
        next_page_link = response.xpath('//ul[@class="pagination pagination-sm"]/li[@class="page"]/a[text()="Next"]/@href').get()
        if next_page_link:
            next_page_url = response.urljoin(next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse)
    
    def parse_description(self, response):
        item = response.meta['item']
        Description_elements = response.xpath('//div[@class="press-release-content"]/div[@class="tmharticle entry-content"]//text()')
        Description = ' '.join(Description_elements.extract()).strip()
       
        Description = re.sub(r'\s+', ' ', Description)
        item['Description'] = Description  
        yield item
