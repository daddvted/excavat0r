"""
四川旅行社列表
URL: http://www.tsichuan.com/travellist.htm?type=&region=510100&pageNo=1
爬取日期: 2016-7-8
爬取页面: 1 - 41
"""
import sys
import time
import random
import requests
import lxml.html
import mysql.connector
from bs4 import BeautifulSoup
from spider.Utils import fake_useragent


class TravelAgencySpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

        self.headers = {}

    def save2db(self, data):
        template = "INSERT INTO travel_agency(name, license, type, addr, tel, zip, email, website, route) " \
                   "VALUES (%(name)s, %(license)s, %(type)s, %(addr)s, %(tel)s, %(zip)s, %(email)s, %(website)s, %(route)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def crawl(self, start):
        base_url = "http://www.tsichuan.com/{0}"
        url = "http://www.tsichuan.com/travellist.htm?type=&region=510100&pageNo={0}"
        for m in range(start, 41):
            print("====== Processing page {0} ======".format(m))
            browser = requests.post(url.format(m))
            if browser.status_code == 200:
                root = lxml.html.fromstring(browser.text)
                links = root.xpath('//div[@class="wzsc_lxs_list"]/dl/dd/h3/a')
                for link in links:
                    new_url = base_url.format(link.attrib["href"])
                    self.crawl2(new_url)
            else:
                print("Error when crawling page {0}".format(m))

    def crawl2(self, url):
        print("processing: {0}".format(url))
        self.headers["User-Agent"] = fake_useragent()
        browser = requests.get(url, headers=self.headers)
        if browser.status_code == 200:
            # root = lxml.html.fromstring(browser.text)
            # lis = root.xpath('//ul[@class="wzsc_bgjd_cs_jbxx"]/li')

            root = BeautifulSoup(browser.text, 'lxml')
            lis = root.find('ul', class_="wzsc_bgjd_cs_jbxx").find_all("li")

            tp = lis[2].contents[1].strip('\r\n').replace('\t', '').replace(' ', '').strip('\r\n').replace('\r\n', ',')
            link = lis[7].find('a')
            website = link.get("href") if link else "#"
            route = root.find_all("div", class_="wzsc_bgjd_cs_p contoxt")[1].text.strip()

            data = {
                "name": str(lis[0].contents[1]) if len(lis[0].contents) > 1 else "",
                "license": str(lis[1].contents[1]) if len(lis[1].contents) > 1 else "",
                "type": tp,
                "addr": str(lis[3].contents[1]) if len(lis[3].contents) > 1 else "",
                "tel": str(lis[4].contents[1]) if len(lis[4].contents) > 1 else "",
                "zip": str(lis[5].contents[1]) if len(lis[5].contents) > 1 else "",
                "email": str(lis[6].contents[1]) if len(lis[6].contents) > 1 else "",
                "website": website,
                "route": route
            }
            self.save2db(data)

        else:
            print("Error when processing url: {0}".format(url))
        time.sleep(random.randint(1, 3))


if __name__ == "__main__":
    start = sys.argv[1]
    spider = TravelAgencySpider()
    spider.crawl(int(start))

    spider.cursor.close()
    spider.conn.close()
