# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import time
import hashlib
import requests
import socket

class BooksSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BooksDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """
        proxy = self.get_proxy()
        print("this is request ip:" + proxy)
        request.meta['proxy'] = proxy
        url, port = self.get_proxy()
        ip = socket.gethostbyname(url)
        proxy = ip + ':' + port
        request.meta['proxy'] = proxy
        """
        pass

    def process_response(self, request, response, spider):
        con = response.text
        if '检测到有异常' in con:
            proxy = self.get_proxy()
            print("this is request ip:" + proxy)
            request.meta['proxy'] = proxy
            return request
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    @classmethod
    def get_proxy(self):
        t = time.time()
        timestamp = str((int(round(t * 1000))))
        username = 'hyshviehi5899_test'
        password = '12345678'
        md5 = username + password + timestamp
        h1 = hashlib.md5()
        h1.update(md5.encode(encoding='utf-8'))
        md5 = h1.hexdigest()
        # url = 'http://ip1.feiyiproxy.com:88/open?user_name=' + username + '&timestamp=' + timestamp + '&md5=' + md5 + '&pattern=json&number=1'
        url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&pack=20731&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
        re =requests.get(url)
        re =re.json()
        ip = re['data'][0]['ip']
        port = str(re['data'][0]['port'])
        result = ip + ':' + port
        return result


