from scrapy import cmdline
name = 'books'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
