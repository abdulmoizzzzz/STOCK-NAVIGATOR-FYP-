import scrapy
import re
from RaskmediaAustralia.items import RaskmediaaustraliaItem

class RaskSpiderSpider(scrapy.Spider):
    name = "rask_spider"
    allowed_domains = ["www.raskmedia.com.au"]
    start_urls = ["https://www.raskmedia.com.au/investing/todays-news/"]
    scraped_items_count = 0
    max_items_to_scrape = 260

    def parse(self, response):
        news = response.css('.elementor-widget-archive-posts .elementor-post__text')
        source_name = "RaskMedia"  
        for new in news:
            if self.scraped_items_count >= self.max_items_to_scrape:
                self.logger.info(f"Reached maximum limit of {self.max_items_to_scrape} items. Stopping scraping.")
                break

            title = new.css('.elementor-post__title a::text').get().strip()
            publisher_name = new.css('.elementor-post-author::text').get()
            published_date = new.css('.elementor-post-date::text').get().strip()
            title_link = new.css('.elementor-post__title a::attr(href)').get()
            
            # Performing null check before calling .strip()
            publisher_name = publisher_name.strip() if publisher_name else None
            
            yield scrapy.Request(title_link, callback=self.parse_article, meta={'title': title,
                                                                                  'publisher_name': publisher_name,
                                                                                  'published_date': published_date,
                                                                                  'source_name': source_name,
                                                                                  'title_link': title_link})  # Pass source_name and title_link to parse_article
            
            self.scraped_items_count += 1

        
        self.logger.info(f'Source: {source_name}')

        # Pagination
        next_page = response.css('a.page-numbers.next::attr(href)').get()
        if next_page is not None and self.scraped_items_count < self.max_items_to_scrape:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response):
        title = response.meta.get('title')
        publisher_name = response.meta.get('publisher_name')
        published_date = response.meta.get('published_date')
        source_name = response.meta.get('source_name')  
        title_link = response.meta.get('title_link')  
        
        
        description_xpath_1 = response.xpath('//div[@class="postie-post"]//text()').extract()
        description_xpath_2 = response.xpath('//div[@class="elementor-widget-container"]//p[not(contains(text(), "passive income")) and not(contains(text(), "INSTANTLY")) and not(contains(text(), "FREE")) and not(contains(text(), "Psst."))]//text() | //div[@class="elementor-widget-container"]//h2[not(contains(text(), "passive income")) and not(contains(text(), "INSTANTLY")) and not(contains(text(), "FREE")) and not(contains(text(), "Psst."))]//text()').extract()
        
        # Removing HTML tags and newline characters from each description
        description_1 = ' '.join(desc.strip() for desc in description_xpath_1 if desc.strip())
        description_2 = ' '.join(desc.strip() for desc in description_xpath_2 if desc.strip())
        
        
        yield {
            'source_name': source_name, 
            'title': title,  
            'title_link': title_link,
            'publisher_name': publisher_name,
            'published_date': published_date,
            'Description': description_1,
            'Description': description_2,
            
        }
