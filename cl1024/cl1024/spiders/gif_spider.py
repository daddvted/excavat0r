import json
import re
import scrapy

from cl1024.items import GIFItem

class CLGIFSpider(scrapy.Spider):
    name = "gif"
    #allowed_domains = ["1024.com"]

    #prefix = "http://cl.loei.pw/"
    #prefix = "http://cl.clos.me/"
    prefix = "http://cl.bacl.biz/"

    start_urls = []
    url = prefix + "thread0806.php?fid=7&search=&page="
    # crawl only page 1-2

    page = 0
    for i in range(1,5):
        start_urls.append(url+str(i))
    #item = GIFItem()

    def parse(self,response):
        for sel in response.xpath('//table[@id="ajaxtable"]/tbody/tr/td[2]/h3'):
            title_obj = sel.xpath('a/text()').extract()
            url_obj = sel.xpath('a/@href').extract()
            if title_obj:
                title = title_obj[0]

                # Filter the title with 'gif|GIF'
                robj = re.compile('gif',re.I)
                result = robj.search(title)
                if result:
                    link = self.prefix+url_obj[0]
                    return scrapy.Request(link,callback=self.keep_crawling,dont_filter=True)

    def keep_crawling(self,response):
        item = GIFItem()
        item['title'] = response.xpath('//title/text()').extract()[0]
        for sel in response.xpath('//img/@src'):
            item['link'] = sel.extract()
            yield item

