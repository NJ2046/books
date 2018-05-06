import scrapy
from books.items import MovieItem
from books.items import bookitem


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


class books(scrapy.Spider):
    name = 'books'
    allowed_domain = ['book.douban.com/']
    start_urls = ['https://book.douban.com/subject_search?search_text=%E8%BF%BD%E6%9D%80%E4%B8%98%E6%AF%94%E7%89%B9&cat=1001']

    def parse(self, response):
        if 'srarch' in response.url:
            selector = scrapy.Selector(response)
            books = selector.xpath('//div[@class="item_root"')
            for book in books:
                next_page = book.xpath('./a/@href').extract()[0]
                if next_page:
                    yield scrapy.Request(next_page, callback=self.parse)
                break
        else:
            item = bookitem()
            sel = scrapy.Selector(response)
            e = sel.xpath("//div[@id='wrapper']")
            item['b_name'] = e.xpath("./descendant::h1/descendant::span/text()").extract()
            # item['b_img_url'] = e.xpath('.//a[@class="nbg"]@href').extract()
            yield item

