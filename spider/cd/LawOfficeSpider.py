"""
律师事务所查询
URL: http://www.cdslsxh.org/search/Law.aspx?page=1
爬取日期: 2016-7-6
爬取页面: 1-97
"""
import re
import random
import time
import requests
import lxml.html
import mysql.connector
from spider.Utils import fake_useragent


class LawOfficeSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }
    url = "http://www.cdslsxh.org/search/Law.aspx?page={0}"

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def save2db(self, data):

        template = ("INSERT INTO law_office(office_name, competent_bureau, license, telephone, address, director) "
                    "VALUES (%(office_name)s, %(competent_bureau)s, %(license)s, %(telephone)s, "
                    "%(address)s, %(director)s)")
        self.cursor.execute(template, data)
        self.conn.commit()

    def crawl(self):
        for m in range(21, 98):
            print("====== Processing page {0} ======".format(m))

            headers = {
                "User-Agent": fake_useragent()
            }
            browser = requests.get(self.url.format(m), headers=headers)

            if browser.status_code == 200:
                root = lxml.html.fromstring(browser.text)
                divs = root.xpath('//div[@class="info"]')
                for div in divs:
                    data = {}
                    data["office_name"] = div.xpath("./h2")[0].text_content().strip()
                    data["competent_bureau"] = div.xpath("./p[1]")[0].text_content().strip().split(r'：')[1]
                    data["license"] = div.xpath("./p[2]")[0].text_content().strip().split(r'：')[1]
                    line = div.xpath("./p[3]")[0].text_content().strip()
                    tmp = re.split(r'\xa0\xa0\xa0\xa0', line)
                    data["telephone"] = tmp[0].split(r'：')[1]
                    data["address"] = tmp[1].split(r'：')[1]
                    data["director"] = div.xpath("./p[4]")[0].text_content().strip().split(r'：')[1]
                    self.save2db(data)
            else:
                print("Error when crawling page {0}".format(m))

            time.sleep(random.randint(2, 6))


if __name__ == "__main__":
    spider = LawOfficeSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()
