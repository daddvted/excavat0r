"""
成都市民政局- 城乡社区日间照料中心(可用于其它页面爬取)
URL: http://www.cdmzj.gov.cn/cdmz/mzhy/mzhy_rjzl/index.html
爬取日期: 2016-8-10
"""
import random
import time
import lxml.html
import mysql.connector
import requests
from spider.Utils import fake_useragent


class DaytimeCareCenterSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,
    }
    url = "http://www.cdmzj.gov.cn/cdmz/mzhy/mzhy_rjzl/index{}.html"

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def save2db(self, data):

        template = ("INSERT INTO daytime_care_center(name, addr, tel, operation) "
                    "VALUES (%(name)s, %(addr)s, %(tel)s, %(operation)s)")
        self.cursor.execute(template, data)
        self.conn.commit()

    def crawl(self):
        for p in range(2, 39):
            print("====== Processing page {0} ======".format(p))

            headers = {
                "User-Agent": fake_useragent()
            }
            browser = requests.get(self.url.format(p), headers=headers)

            if browser.status_code == 200:
                root = lxml.html.fromstring(browser.text)
                lis = root.xpath('//div[@class="right_message"]/div[@class="right_hy"]/ul/li')
                for li in lis:
                    data = {
                        "name": li.xpath('.//div[@class="right_hy_into_name"]')[0].text_content().strip(),
                        "addr": li.xpath('.//div[@class="right_hy_into_zydz"]/span[1]')[0].text_content().strip(),
                        "tel": li.xpath('.//div[@class="right_hy_into_zydz"]/span[2]')[0].text_content().strip(),
                        "operation": li.xpath('.//div[@class="right_hy_into_zydz"]/span[3]')[0].text_content().strip(),
                    }
                    self.save2db(data)
            else:
                print("Error when crawling page {0}".format(p))

            time.sleep(random.randint(1, 2))


if __name__ == "__main__":
    spider = DaytimeCareCenterSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()
