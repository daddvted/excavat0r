"""
住房保障项目查询
URL: http://www.cdfgj.gov.cn/IHProject/ShowIHProjectList.aspx
"""
import time
import random
import requests
import lxml.html
import mysql.connector
from urllib.parse import urlencode


class HousingEnsuringProjSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }
    url = "http://www.cdfgj.gov.cn/IHProject/ShowIHProjectList.aspx"

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def save2db(self, data):

        template = ("INSERT INTO housing_ensuring_proj"
                    "(project, area, type, addr, start_time, completion_time, status) "
                    "VALUES (%(project)s, %(area)s, %(type)s, %(addr)s, %(start_time)s, "
                    "%(completion_time)s, %(status)s)")
        self.cursor.execute(template, data)
        self.conn.commit()

    def crawl(self):
        for p in range(1, 8):
            print("====== Processing page {0} ======".format(p))
            data = {
                '__EVENTTARGET': 'ID_ucShowIHProjectList$UcNewsListPager1$UcPager1$btnPage{}'.format(p),
                '__VIEWSTATE': '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',
                '__VIEWSTATEGENERATOR': 'E0765F93',
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "NETSCAPE_ID=d2xvvo55pwzvyg2wyxvggziw",
            }
            browser = requests.post(self.url, headers=headers, data=urlencode(data))

            if browser.status_code == 200:
                root = lxml.html.fromstring(browser.text)
                trs = root.xpath('//table[@id="ID_ucShowIHProjectList_UcNewsListPager1_listProject"]/tr')
                for n in range(1, len(trs)):
                    tds = trs[n].xpath('.//td')

                    td0 = tds[0].xpath('./a')[0].attrib
                    project = td0["title"] if "title" in td0 else tds[0].text_content().strip()

                    td2 = tds[2].xpath('./span')[0].attrib
                    tp = td2["title"] if "title" in td2 else tds[2].text_content().strip()

                    td3 = tds[3].xpath('./span')[0].attrib
                    addr = td3["title"] if "title" in td3 else tds[3].text_content().strip()

                    data = {
                        "project": project,
                        "area": tds[1].text_content().strip(),
                        "type": tp,
                        "addr": addr,
                        "start_time": tds[4].text_content().strip(),
                        "completion_time": tds[5].text_content().strip(),
                        "status": tds[6].text_content().strip()
                    }
                    self.save2db(data)

            else:
                print("Error when crawling page {0}".format(p))


if __name__ == "__main__":
    spider = HousingEnsuringProjSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()
