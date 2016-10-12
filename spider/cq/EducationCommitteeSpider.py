"""
区县教委信息查询
URL: http://www.cqedu.cn/Category_152/Index.aspx
"""
import random
import urllib.request
import lxml.html
import mysql.connector

from spider.Utils import fake_useragent


class EducationCommitteeSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service_cq',
        'raise_on_warnings': True,

    }

    def __init__(self):
        # Init mysql
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

        self.header = {
            "User-Agent": fake_useragent()
        }

    def save2db(self, data):
        template = "INSERT INTO educommittee(name, addr, website) " \
                   "VALUES (%(name)s, %(addr)s, %(website)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def prepare2crawl(self):
        url = "http://www.cqedu.cn/Category_152/Index.aspx"
        
        req = urllib.request.Request(url, method="GET")
        resp = urllib.request.urlopen(req)
        
        if resp.status == 200:
            html = lxml.html.fromstring(resp.read().decode("utf-8"))
            tables = html.xpath('//table[@id="uc_ctlSchoolList.ascx_DataList1"]//table')
            for table in tables:
                a = table.xpath('.//a')[0]
                data = {
                    "name": a.text_content().strip(),
                    "addr": table.xpath('.//span')[0].text_content().strip(),
                    "website": a.attrib["href"]
                }
                self.save2db(data)
        else:
            print("Error")

    def crawl(self, page):
        pass

    def final_crawl(self):
        pass

if __name__ == "__main__":
    spider = EducationCommitteeSpider()
    spider.prepare2crawl()

    spider.cursor.close()
    spider.conn.close()
