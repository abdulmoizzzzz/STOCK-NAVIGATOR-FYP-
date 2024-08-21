import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from BenzingaproUSA.items import BenzingaprousaItem

class BenzingaSpiderSpider(scrapy.Spider):
    name = "Benzinga_spider"
    allowed_domains = ["www.benzinga.com"]
    start_urls = ["https://www.benzinga.com/markets"]
    source_name = "Benzinga"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,  
    }

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.item_count = 0 

    def parse(self, response):
        self.driver.get(response.url)
        sleep(2)

        sel = Selector(text=self.driver.page_source)
        news_items = sel.css('.content-feed-list a.newsfeed-card')
        
        for news in news_items:
            title = news.css('span::text').get()
            title_link = news.css('::attr(href)').get()

            yield scrapy.Request(title_link, callback=self.parse_news,
                                 meta={'title': title, 'title_link': title_link})

            self.item_count += 1  

            if self.item_count >= 450:
                self.logger.info("Scraped 450 items. Stopping the scraping process.")
                break

    def parse_news(self, response):
        item = BenzingaprousaItem()
        item['source_name'] = self.source_name
        item['title'] = response.meta['title']
        item['title_link'] = response.meta['title_link']
        item['published_date'] = response.css('.date::text').get()
        item['publisher_name'] = response.css('.author-name::text').get()
        item['Description'] = ''.join(response.xpath('//p[@class="block core-block"]//text()').getall())

        yield item

    def closed(self, reason):
        self.driver.quit()
