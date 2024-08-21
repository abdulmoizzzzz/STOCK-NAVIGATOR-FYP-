import scrapy
import re
from SimplywallGermany.items import SimplywallgermanyItem

class SimplywallSpiderSpider(scrapy.Spider):
    name = "simplywall_spider"
    allowed_domains = ["simplywall.st"]
    start_urls = ["https://simplywall.st/news/de"]
    source_name = "Simply Wall St"
    item_count = 0 

    def parse(self, response):
       
        news = response.css('.hKrXFX')
        for new in news:
            item = SimplywallgermanyItem()
            item['source_name'] = self.source_name 
            item['title'] = new.css('.gumIZl::text').get()
            item['title_link'] = new.css('div.sc-6fdf01d2-2.hKrXFX > a:nth-of-type(3)::attr(href)').get()
            item['published_date'] = new.css('div.sc-6fdf01d2-4.iVGIen > time::attr(datetime)').get()
            
            yield scrapy.Request(item['title_link'], callback=self.parse_article, meta={'item': item})

            self.item_count += 1  
            if self.item_count >= 200: 
                self.logger.info("Reached 100 news items. Stopping the spider.")
                return 

        # Handling pagination
        next_page_relative_url = response.xpath('//a[span[text()="Next"]]/@href').get()
        if next_page_relative_url is not None:
            next_page_url = response.urljoin(next_page_relative_url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response):
        item = response.meta['item']
        description = response.xpath('//div[@data-cy-id="article-content"]//text()').getall()
        cleaned_description = ' '.join(description)
        cleaned_description = re.sub(r'\s+', ' ', cleaned_description)  
        item['Description'] = cleaned_description.strip()
        yield item

        self.item_count += 1  
        if self.item_count >= 200: 
            self.logger.info("Reached 100 news items. Stopping the spider.")
            return
