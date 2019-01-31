"""
免费药具发放点查询
URL: http://www.cqwsjsw.gov.cn/Html/1/mfyjff/index.html
"""
import time
import random
import urllib.request
import lxml.html
import mysql.connector
from service_api.Utils import fake_useragent


class FreeMedicineSpider(object):
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

    def save2db(self, data):
        template = "INSERT INTO freemedicine(area, street_town, community_village, work_time, service_tel, complaint_tel) " \
                   "VALUES (%(area)s, %(street_town)s, %(community_village)s, %(work_time)s, %(service_tel)s, %(complaint_tel)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def prepare2crawl(self, start):
        url = "http://www.cqwsjsw.gov.cn/wsfw/yjff.aspx?flag=sel&seldq=0&pageNo={}"

        # for p in range(start, 704):
        for p in range(704, 705):
            print("------ Processing page {} ------".format(p))
            header = {
                "User-Agent": fake_useragent()
            }

            req = urllib.request.Request(url.format(p), headers=header, method="GET")
            resp = urllib.request.urlopen(req)

            if resp.status == 200:
                html = lxml.html.fromstring(resp.read().decode("gbk"))
                # html = lxml.html.fromstring(resp.read().decode("gb18030"))
                tables = html.xpath('//td[@height="34"]/table')
                for n in range(1, len(tables)):
                    tds = tables[n].xpath('.//td')
                    data = {
                        "area": tds[1].text_content().strip(),
                        "street_town": tds[2].text_content().strip(),
                        "community_village": tds[3].text_content().strip(),
                        "work_time": tds[4].text_content().strip(),
                        "service_tel": tds[5].text_content().strip(),
                        "complaint_tel": tds[6].text_content().strip(),
                    }
                    # print(data)
                    self.save2db(data)
            else:
                print("Error processing page {}".format(p))
                break
            print("------ Finish page {} ------".format(p))
            time.sleep(random.randint(1, 3))

    def crawl(self, page):
        pass

    def final_crawl(self):
        pass

if __name__ == "__main__":
    spider = FreeMedicineSpider()
    spider.prepare2crawl(1)

    spider.cursor.close()
    spider.conn.close()
