"""
律师查询
URL: http://www.cdslsxh.org/lawyer/1.html
爬取日期: 2016-7-6
爬取页面: 1.html - 9499.html
"""
import random
import time

import lxml.html
import mysql.connector
import requests

from spider.Larva import Larva


class LawyerSpider(Larva):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,
    }
    url = "http://www.cdslsxh.org/lawyer/{0}.html"

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def save2db(self, data):

        template = ("INSERT INTO lawyer(name, law_office, gender, license, category) "
                    "VALUES (%(name)s, %(law_office)s, %(gender)s, %(license)s, %(category)s)")
        self.cursor.execute(template, data)
        self.conn.commit()

    def crawl(self):
        for m in range(1, 9500):
            print("====== Processing page {0} ======".format(m))

            headers = {
                "User-Agent": random.choice(self.USER_AGENTS)
            }
            browser = requests.get(self.url.format(m), headers=headers)

            if browser.status_code == 200:
                root = lxml.html.fromstring(browser.text)
                divs = root.xpath('//div[@class="lawyerinfo"]')
                data = {
                    "name": divs[0].xpath("./h3")[0].text_content().strip(),
                    "law_office": divs[0].xpath('./p[1]')[0].text_content().split('：')[1],
                    "gender": divs[0].xpath('./p[2]')[0].text_content().split('：')[1],
                    "license": divs[0].xpath('./p[3]')[0].text_content().split('：')[1],
                    "category": divs[0].xpath('./p[4]')[0].text_content().split('：')[1],
                }
                self.save2db(data)
            else:
                print("Error when crawling page {0}".format(m))

            time.sleep(random.randint(1, 2))


if __name__ == "__main__":
    spider = LawyerSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()
