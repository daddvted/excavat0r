"""
物理管理执业名册
URL: http://zy.cdpma.cn/C_staffSearch/EnterPriseInfo.aspx
"""
import sys
import time
import random
import requests
import lxml.html
import mysql.connector
from urllib.parse import urlencode
from spider.LarvaSpider import Larva


class PropertyMngSpider(Larva):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }

    URL = "http://zy.cdpma.cn/C_staffSearch/EnterPriseInfo.aspx"
    BASE_URL = "http://www.cdcc.gov.cn/QualitySafeShow/"

    def __init__(self, start):
        self.start_page = start
        self.total_page = 242

        self.__VIEWSTATE = ""
        self.__EVENTTARGET = ""

        # Init mysql
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def save2db(self, data):

        template = "INSERT INTO property_mng(name, area, addr, level) " \
                   "VALUES (%(name)s, %(area)s, %(addr)s, %(level)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    # 1st crawl, get total
    def crawl(self):
        print("crawling page 1")
        headers = {
            "User-Agent": random.choice(self.USER_AGENTS)
        }
        browser = requests.get(self.URL, headers=headers)
        if browser.status_code == 200:
            html = lxml.html.fromstring(browser.text)

            view_state_div = html.xpath('//input[@id="__VIEWSTATE"]')
            self.__VIEWSTATE = view_state_div[0].attrib["value"]
            self.__EVENTTARGET = "pagerExhibit"

            self.crawl2()

        else:
            print("Error while crawling page 1")

    def crawl2(self):
        for p in range(self.start_page, self.total_page + 1):
            time.sleep(random.randint(1, 3))

            data = {
                "__VIEWSTATE": self.__VIEWSTATE,
                "__EVENTARGUMENT": p,
                "__EVENTTARGET": self.__EVENTTARGET,
            }

            print("crawling page {}".format(p))
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": random.choice(self.USER_AGENTS),
            }
            browser = requests.post(self.URL, headers=headers, data=urlencode(data))
            if browser.status_code == 200:
                html = lxml.html.fromstring(browser.text)
                trs = html.xpath('//table[@id="DataGrid1"]/tr')
                for n in range(1, len(trs)):
                    tds = trs[n].xpath('.//td')
                    data = {
                        "name": tds[1].text_content().strip(),
                        "area": tds[2].text_content().strip(),
                        "addr": tds[3].text_content().strip(),
                        "level": tds[4].text_content().strip(),
                    }
                    print(data)
                    self.save2db(data)
            else:
                print("Error while crawling page {}".format(p))

if __name__ == "__main__":
    start_page = sys.argv[1] if len(sys.argv) > 1 else 1
    spider = PropertyMngSpider(int(start_page))
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()

