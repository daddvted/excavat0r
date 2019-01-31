"""
四川旅行社列表
URL: http://www.tsichuan.com/travellist.htm?type=&region=510100&pageNo=1
爬取日期: 2016-7-8
爬取页面: 1 - 41
"""
import time
import random
import requests
import lxml.html
import mysql.connector
from service_api.Utils import fake_useragent


class JucicialOrgSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.1.172',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

        self.headers = {}

    def save2db(self, data):
        template = "INSERT INTO judicial_org(name, license, director, representative, business, area, admin_org, " \
                   "addr, fax, zip, tel, num) VALUES (%(name)s, %(license)s, %(director)s, %(representative)s," \
                   " %(business)s, %(area)s, %(admin_org)s, %(addr)s, %(fax)s, %(zip)s, %(tel)s, %(num)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def crawl(self):
        base_url = "http://www.cdjustice.chengdu.gov.cn{0}"
        url = "http://www.cdjustice.chengdu.gov.cn/cdsfjmis/sfjd/sfjd-oper-type!findSel.action"
        data = {
            "pageNo": 1,
            "pageSize": 40,
        }
        print("====== Processing page {0} ======".format(1))
        browser = requests.post(url, data=data)
        if browser.status_code == 200:
            root = lxml.html.fromstring(browser.text)
            links = root.xpath('//table[@id="ctl00_ContentPlaceHolder2_GridView1"]/tr/td[1]/a')

            for link in links:
                new_url = base_url.format(link.attrib["href"])
                self.crawl2(new_url)
        else:
            print("Error when crawling page {0}".format(1))

    def crawl2(self, url):
        print("processing: {0}".format(url))
        self.headers["User-Agent"] = fake_useragent()
        browser = requests.get(url, headers=self.headers)
        if browser.status_code == 200:
            root = lxml.html.fromstring(browser.text)
            tds = root.xpath('//div[@id="myTab0_Content0"]/table/tr/td')

            data = {
                "name": str(tds[1].text_content()).strip(),
                "license": str(tds[3].text_content()).strip(),
                "director": str(tds[5].text_content()).strip(),
                "representative": str(tds[7].text_content()).strip(),
                "business": str(tds[9].text_content()).strip(),
                "area": str(tds[11].text_content()).strip(),
                "admin_org": str(tds[13].text_content()).strip(),
                "addr": str(tds[15].text_content()).strip(),
                "fax": str(tds[17].text_content()).strip(),
                "zip": str(tds[19].text_content()).strip(),
                "tel": str(tds[21].text_content()).strip(),
                "num": str(tds[23].text_content()).strip(),
            }
            self.save2db(data)

        else:
            print("Error when processing url: {0}".format(url))
        time.sleep(random.randint(1, 3))


if __name__ == "__main__":
    spider = JucicialOrgSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()
