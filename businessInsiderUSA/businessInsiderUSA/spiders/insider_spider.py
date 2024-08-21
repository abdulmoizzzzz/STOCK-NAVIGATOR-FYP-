import scrapy
from businessInsiderUSA.items import BusinessinsiderusaItem
from businessInsiderUSA.itemloaders import BusinessProductLoader

class InsiderSpiderSpider(scrapy.Spider):
    name = "insider_spider"
    allowed_domains = ["markets.businessinsider.com"]
    start_urls = ["https://markets.businessinsider.com/news?p=1"]
    source_name = "BusinessInsider"
    def parse(self, response):
        news = response.css('.image-news-list__story')
        for news_item in news:
            title = news_item.css('.latest-news__title::text, .image-news-list__link::text').get().strip()
            title_link = news_item.css('h3.image-news-list__title a.image-news-list__link::attr(href)').get()
            if title_link:
                yield response.follow(title_link, callback=self.parse_news, meta={'title': title})

        news = response.css('.latest-news__story')
        for news_item in news:
            title = news_item.css('.latest-news__title a.latest-news__link::text').get()
            title_link = news_item.css('.latest-news__title a.latest-news__link::attr(href)').get()
            if title_link:
                yield response.follow(title_link, callback=self.parse_news, meta={'title': title})

        next_page = response.css('li.pagination__item[title="Goto Page 2"] a.pagination__text[href*="?p=2"]::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_news(self, response):
        

        # Scraping news details
        loader = BusinessProductLoader(BusinessinsiderusaItem(), response=response)
        loader.add_value('source_name', self.source_name)
        loader.add_value('title', response.meta.get('title'))
        loader.add_value('title_link', response.url)

        description_parts = response.css('ul.summary-list strong::text, p strong::text, p em::text, p i::text, p u::text, p::text, p a::text').getall()
        description = ' '.join(description_parts)
        loader.add_value('Description', description)

        yield loader.load_item()
