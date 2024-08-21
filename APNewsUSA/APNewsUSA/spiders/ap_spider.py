import scrapy
from APNewsUSA.items import ApnewsusaItem

class ApSpiderSpider(scrapy.Spider):
    name = "ap_spider"
    allowed_domains = ["apnews.com"]
    start_urls = ["https://apnews.com/hub/financial-markets"]

    def parse(self, response):
        news_list = response.css('.PageList-items-item')

        for news in news_list[5:]:
            title = news.css('.PagePromo-title .PagePromoContentIcons-text::text').get()
            title_link = news.css('.PagePromo-title a::attr(href)').get()

            
            yield response.follow(title_link, self.parse_news, meta={'title': title, 'title_link': title_link})

    def parse_news(self, response):
        item = ApnewsusaItem()  

        item['title'] = response.meta['title']
        item['title_link'] = response.meta['title_link']
        item['published_by'] = response.css('.Page-authors').xpath('translate(normalize-space(), "\xa0", " ")').get().strip() 
        item['Description'] = ''.join(response.xpath('//p//text()').getall()).strip() 
         

        yield item  
