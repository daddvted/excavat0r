"""
宗教查询
URL: http://www.cdmzzj.gov.cn/news.do?method=getTWebCoreArticlePageQuery&channelId=channelId201308271454054502532096
"""
import re
import requests
import lxml.html
import mysql.connector
from urllib.parse import urlencode
from service_api.Utils import fake_useragent


class ReligionSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }

    URL = "http://www.cdmzzj.gov.cn/news.do?method=getTWebCoreArticlePageQuery&channelId=channelId201308271454054502532096"
    BASE_URL = "http://www.cdmzzj.gov.cn"

    def __init__(self):
        # Init mysql
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def save2db(self, data):

        template = "INSERT INTO religion(name, type, intro) " \
                   "VALUES (%(name)s, %(type)s, %(intro)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    # 1st crawl, get total
    def crawl(self):
        data = {
            "pres_curPage": 1,
            "pres_rows": 200,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        browser = requests.post(self.URL, headers=headers, data=urlencode(data))

        if browser.status_code == 200:
            html = lxml.html.fromstring(browser.text)
            trs = html.xpath('//*[@id="pageDispatchFrom"]/table[1]/tr')
            print(len(trs))
            for tr in trs:
                a = tr.xpath('.//td/a')
                link = self.BASE_URL + a[0].attrib["href"]

                text = tr.xpath('./td[1]')[0].text_content().strip()
                m = re.findall(r'【(.*)】(.*)', text)

                self.crawl2(link, m[0])
        else:
            print("Error while crawling page 1")

    def crawl2(self, url, msg):
        print("processing url: {}".format(url))
        headers = {
            "User-Agent": fake_useragent()
        }
        browser = requests.get(url, headers=headers)
        if browser.status_code == 200:
            html = lxml.html.fromstring(browser.text)
            td = html.xpath('//*[@id="main_body"]/div[2]/table/tr/td/table/tr[2]/td/table/tr[5]/td')
            intro = str(td[0].text_content())

            data = {
                "name": msg[0],
                "type": msg[1],
                "intro": intro,
            }
            self.save2db(data)

        else:
            print("Error while crawling page {}".format(p))

if __name__ == "__main__":
    spider = ReligionSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()

