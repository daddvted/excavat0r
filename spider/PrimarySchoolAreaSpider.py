"""
成都市小学新生入学划片区域
URL: http://www.chengdu.gov.cn/servicelist/xxjy04/
"""

import requests
import lxml.html
import mysql.connector


class FixServeOrgSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }
    url = "http://www.chengdu.gov.cn/servicelist/xxjy04/"

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def save2db(self, data):
        template = "INSERT INTO issue_org(org_name, issue_type, province) " \
                   "VALUES ('{org_name}', '{issue_type}', '{province}')"
        sql = template.format(**data)
        self.cursor.execute(sql)
        self.conn.commit()

    def crawl(self):
        print("====== Processing page {0} ======".format(1))
        browser = requests.get(self.url)
        browser.encoding = "utf-8"

        if browser.status_code == 200:
            root = lxml.html.fromstring(browser.text)
            tables = root.xpath('//*[@class="article-content-ex"]/table')
            strongs = root.xpath('//*[@style="font-size: 24px;"]')
            num = len(strongs)
            for n in range(num):
                district = strongs[n].text_content().strip()
                trs = tables[n].xpath('.//tr')
                for m in range(1, len(trs)):
                    tds = trs[m].xpath('.//td')
                    print(tds[1].text_content())
                    print(tds[2].text_content())
                    print(tds[3].text_content())


                # print(district, ":", len(trs))





        else:
            print("Error when crawling page {0}".format(1))


if __name__ == "__main__":
    spider = FixServeOrgSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()
