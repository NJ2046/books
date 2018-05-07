# coding:utf-8
import scrapy
from books.items import MovieItem
from books.items import bookitem
from selenium import webdriver
import re

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
    start_urls = list()
    with open('../data/input/200', 'r', encoding='utf-8') as rd:
        for line in rd:
            start_urls.append(line.strip())

    def __init__(self):
        self.browser = webdriver.Chrome("C:\\Users\\NJ\Desktop\\test\\chromedriver.exe")

    def parse(self, response):
        item = bookitem()
        self.browser.get(response.url)
        if 'search' in response.url:
            """
            selector = scrapy.Selector(response)
            books = selector.xpath("//div[@class='item-root']")
            """
            books = self.browser.find_elements_by_xpath('//div[@class="item-root"]')
            if books:
                if len(books) > 7:
                    for i in range(len(books)):
                        if i > 0:
                            a = books[i].find_element_by_xpath('./a')
                            next_page = a.get_attribute('href')
                            if next_page:
                                yield scrapy.Request(next_page, callback=self.parse)
                                break
                else:
                    for i in range(len(books)):
                        a = books[i].find_element_by_xpath('./a')
                        next_page = a.get_attribute('href')
                        if next_page:
                            yield scrapy.Request(next_page, callback=self.parse)
                            break
            else:
                pass
        else:
            sel = scrapy.Selector(response)
            e = sel.xpath("//div[@id='wrapper']")
            publish = '出版社[^\u4e00-\u9fa5]*([\u4e00-\u9fa5]+)'
            price = '定价[^\d]*([\d]+.[\d]+)'
            ISBN = 'ISBN[^\d]*([\d]+)'
            writer = '作者[^\u4e00-\u9fa5]*([\u4e00-\u9fa5]+)'
            bkinfor = e.xpath('//*[@id="info"]').extract()
            bkinfor = bkinfor[0]
            # publish
            p1 = re.compile(publish)
            m1 = p1.findall(bkinfor)
            item['b_publish'] = m1
            # price
            p1 = re.compile(price)
            m1 = p1.findall(bkinfor)
            item['b_price'] = m1
            # ISBN
            p1 = re.compile(ISBN)
            m1 = p1.findall(bkinfor)
            item['b_isbn'] = m1
            # writer
            p1 = re.compile(writer)
            m1 = p1.findall(bkinfor)
            item['b_writer'] = m1

            item['b_d_name'] = e.xpath("./descendant::h1/descendant::span/text()").extract()
            item['b_ps'] = e.xpath('//*[@id="link-report"]/div[1]/div/p/text()').extract()
            item['b_img_url'] = e.xpath('//*[@id="mainpic"]/a/@href').extract()[0]
            # 为成功提取
            yield item

