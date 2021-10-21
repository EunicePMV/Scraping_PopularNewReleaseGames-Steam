import scrapy
from scrapy.http import Request

class GamesSpider(scrapy.Spider):
    name = 'games'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?filter=popularnew&sort_by=Released_DESC&os=win']

    def parse(self, response):
        games = response.xpath("//div[@id='search_resultsRows']//a")
        for game in games:
            game_name = game.xpath(".//div/span[@class='title']/text()").get()
            platform = game.xpath(".//div/span[@class='title']/following-sibling::p/span/@class").getall()

            if game.xpath(".//div[@class='col search_discount responsive_secondrow']/following-sibling::div/span/following-sibling::text()").get():
                price = game.xpath(".//div[@class='col search_discount responsive_secondrow']/following-sibling::div/span/following-sibling::text()").get().strip()
            else:
                price = game.xpath(".//div[@class='col search_discount responsive_secondrow']/following-sibling::div/text()").get().strip()

            yield{'name': game_name,
                  'platform': platform,
                  'price': price}

        nxt_page_url = response.xpath("//div[@class='search_pagination_right']//a//@href").getall()[:-1]
        for page_url in nxt_page_url:
            yield Request(page_url,
                          callback=self.parse)