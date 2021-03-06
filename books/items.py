# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    info = scrapy.Field()
    rating = scrapy.Field()
    num = scrapy.Field()
    quote = scrapy.Field()
    img_url = scrapy.Field()


class bookitem(scrapy.Item):
    b_s_name = scrapy.Field()
    b_d_name = scrapy.Field()
    b_isbn = scrapy.Field()
    b_writer = scrapy.Field()
    b_publish = scrapy.Field()
    b_class = scrapy.Field()
    b_price = scrapy.Field()
    b_ps = scrapy.Field()
    b_img_url = scrapy.Field()
