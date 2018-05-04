import scrapy
from books.items import MovieItem


class doubanMovie(scrapy.Spider):
    name = 'doubanMovie'
    allowed_domain = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        selector = scrapy.Selector(response)
        movies = selector.xpath('//div[@class="item"]')
        item = MovieItem()

        for movie in movies:
            titles = movie.xpath('.//span[@class="title"]/text()').extract()
            name = ''
            for title in titles:
                name += title.strip()
            item['name'] = name
            item['img_url'] = movie.xpath('.//img/@src').extract()[0]
            yield item


