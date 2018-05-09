# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import json
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
import pymysql
from logging import log
from books import settings


class MoviePipeline(object):
    def __init__(self):
        self.file = open('data.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        json.dump(dict(item), self.file, ensure_ascii=False)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.file.close()


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['b_img_url'])

    def item_completed(self, results, item, info):
        image_url = [x['path'] for ok, x in results if ok]

        if not image_url:
            raise DropItem('item contains no image')

        item['b_image_url'] = image_url
        return item


class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();

    def process_item(self, item, spider):
        try:
            t = item['b_img_url'].split('/')[-1]
            print('---------------------------------------------------------------------')
            print(t)
            print('---------------------------------------------------------------------')
            # 插入数据
            self.cursor.execute(
                """insert into tmp(name, path)
                value (%s, %s)""",
                (item['name'],
                 item['b_img_url'].split('/')[-1]))

            # 提交sql语句
            self.connect.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            log(error)
        return item


class bookPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();

    def process_item(self, item, spider):
        try:
            # 插入数据
            s = item['b_s_name'][0]
            f = item['b_price'][0]
            name = item['b_d_name'][0]
            pub = item['b_publish'][0]
            isbn = item['b_isbn'][0]
            writer = item['b_writer'][0]
            ps = ''.join(item['b_ps'])
            path = item['b_img_url']
            f = float(f)
            # self.cursor.execute(
            #    """insert into tmp(name, publish, price)
            # value (%s, %s, %f)""",
            #     (item['b_d_name'],
            #     item['b_publish'],
            #     f
            #    ))
            sql = "insert into tmp(name, publish, price, isbn, writer, ps, path) \
            values ('%s', '%s', '%f', '%s', '%s', '%s', '%s')" \
                  % (name, pub, f, isbn, writer, ps, path)
            self.cursor.execute(sql)
            # 提交sql语句
            self.connect.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            log(error, 'wocuole')
        return item

