import scrapy
from NewscomAustralia.items import NewscomaustraliaItem


class NewsSpiderSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = ["www.news.com.au"]
    start_urls = ["https://www.news.com.au/finance/markets/australian-markets"]
    source_name = "news.com.au"
    scraped_items_count = 0
    max_items_to_scrape = 100

    def parse(self, response):
        news = response.css('.storyblock')
        for new in news:
            # Extracting title and title link
            title = new.css('h4.storyblock_title a.storyblock_title_link::text').get()
            title_link = new.css('h4.storyblock_title a.storyblock_title_link::attr(href)').get()
            yield scrapy.Request(title_link, callback=self.parse_news, meta={'title': title})

            
            self.scraped_items_count += 1
            if self.scraped_items_count >= self.max_items_to_scrape:
                self.logger.info(f"Reached maximum limit of {self.max_items_to_scrape} items. Stopping scraping.")
                break

        # pagination
        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page is not None and self.scraped_items_count < self.max_items_to_scrape:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_news(self, response):
        item = NewscomaustraliaItem()
        item['source_name'] = self.source_name
        item["published_date"] = response.css('#publish-date::text').get() # Corrected this line
        publisher_name = response.css('#story-byline .g_font-body-m::text').get()
        
       
        description_xpath = "//p[not(contains(., 'To join the conversation, please'))]//text()"
        description = ' '.join(response.xpath(description_xpath).getall())
        
        # Yielding the complete news item
        yield {
            'source_name': self.source_name,
            'title': response.meta['title'],
            'title_link': response.url,
            'published_date': item["published_date"], 
            'publisher_name': publisher_name,
            'Description': description,
        }
