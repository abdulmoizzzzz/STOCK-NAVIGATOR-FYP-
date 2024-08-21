import scrapy
import re


class CapitalSpiderSpider(scrapy.Spider):
    name = "captial_spider"
    allowed_domains = ["capital.com"]
    start_urls = ["https://capital.com/stock-market-news"]
    source_name = "Capital.com"
    news_count = 0
    max_news_count = 150

    def parse(self, response):
        news = response.css('.main-article-item__content')
        for article in news:
            if self.news_count >= self.max_news_count:
                self.logger.info('Maximum news count reached. Stopping the spider.')
                return
            title = article.css('.main-article-item__title a::text').get()
            title_link = article.css('.main-article-item__title a::attr(href)').get()
            published_date = article.css('.date-posted::text').get()
            author = article.css('.author::text').get()
            yield scrapy.Request(title_link, callback=self.parse_article, meta={'title': title,
                                                                                 'published_date': published_date,
                                                                                 'author': author})

            self.news_count += 1

        next_page = response.css('li.nextBtn a.ln-auto::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response):
        title = response.meta['title']
        published_date = response.meta['published_date']
        author = response.meta['author']
        
        Description = " ".join(response.css('p::text').getall())
        Description = re.sub(r'\s+', ' ', Description).strip()
        yield {
            'source': self.source_name,
            'title': title,
            'title_link': response.url,
            'published_date': published_date,
            'author': author,
            'Description': Description
        }
