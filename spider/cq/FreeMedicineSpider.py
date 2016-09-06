"""
免费药具发放点查询
URL: http://www.cqwsjsw.gov.cn/Html/1/mfyjff/index.html
"""
import re
import random
import urllib.request
import lxml.html
import mysql.connector

from spider.Larva import Larva


class FreeMedicineSpider(Larva):
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
            "User-Agent": random.choice(self.USER_AGENTS)
        }

    def save2db(self, data):
        template = "INSERT INTO educommittee(name, addr, website) " \
                   "VALUES (%(name)s, %(addr)s, %(website)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def prepare2crawl(self, start):
        url = "http://www.cqwsjsw.gov.cn/wsfw/yjff.aspx?flag=sel&seldq=0&pageNo={}"

        # for p in range(start, 704):
        for p in range(start, 2):
            print("------ Processing page {} ------".format(p))
            header = {
                "User-Agent": random.choice(self.USER_AGENTS)
            }

            req = urllib.request.Request(url.format(p), headers=header, method="GET")
            resp = urllib.request.urlopen(req)

            if resp.status == 200:
                html = lxml.html.fromstring(resp.read().decode("gbk"))
                tables = html.xpath('//td[@height="34"]/table')
                for n in range(1, len(tables)):
                    tds = tables[n].xpath('.//td')
                    print(len(tds))
                    data = {
                        "area": tds[1].text_content().strip(),
                        "street_town": tds[2].text_content().strip(),
                        "community_village": tds[3].text_content().strip(),
                        "work_time": tds[4].text_content().strip(),
                        "service_tel": tds[5].text_content().strip(),
                        "complaint_tel": tds[6].text_content().strip(),
                    }
                    print(data)
            else:
                print("Error processing page {}".format(p))
                break

    def crawl(self, page):
        pass

    def final_crawl(self):
        pass

if __name__ == "__main__":
    spider = FreeMedicineSpider()
    spider.prepare2crawl(1)

    spider.cursor.close()
    spider.conn.close()
