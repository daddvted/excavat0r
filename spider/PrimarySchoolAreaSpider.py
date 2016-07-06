"""
成都市小学新生入学划片区域
URL: http://www.chengdu.gov.cn/servicelist/xxjy04/
"""

import requests
import lxml.html
import mysql.connector


class PrimarySchoolAreaSpider(object):
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
        """
        Change this template, refer to EnvProtectionStdSpider
        Change this template, refer to EnvProtectionStdSpider
        Change this template, refer to EnvProtectionStdSpider
        """
        template = "INSERT INTO primary_school_area(school_name, area, district) " \
                   "VALUES (%(school_name)s, %(area)s, %(district)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def crawl(self):
        print("====== Processing page {0} ======".format(1))
        browser = requests.get(self.url)
        browser.encoding = "utf-8"

        if browser.status_code == 200:
            # root = lxml.html.fromstring(browser.text)
            fh = open("cd_primary_school.htm", 'r')
            root = lxml.html.fromstring(fh.read())
            tables = root.xpath('//*[@class="article-content-ex"]/table')
            strongs = root.xpath('//*[@style="font-size: 24px;"]')

            type1 = [0, 1, 3]
            type2 = [2, 4, 5]
            type3 = [6]

            for t in type1:
                district = strongs[t].text_content().strip()
                trs = tables[t].xpath('.//tr')
                for n in range(1, len(trs)):
                    tds = trs[n].xpath('.//td')
                    data = {
                        "school_name": tds[2].text_content().strip(),
                        "area": tds[3].text_content().strip(),
                        "district": district
                    }
                    self.save2db(data)

            for t in type2:
                district = strongs[t].text_content().strip()
                trs = tables[t].xpath('.//tr')
                for n in range(1, len(trs)):
                    tds = trs[n].xpath('.//td')
                    data = {
                        "school_name": tds[1].text_content().strip(),
                        "area": tds[2].text_content().strip(),
                        "district": district
                    }
                    self.save2db(data)

            for t in type3:
                district = strongs[t].text_content().strip()
                trs = tables[t].xpath('.//tr')
                for n in range(1, len(trs)):
                    tds = trs[n].xpath('.//td')
                    data = {
                        "school_name": tds[0].text_content().strip(),
                        "area": tds[5].text_content().strip(),
                        "district": district
                    }
                    self.save2db(data)
        else:
            print("Error when crawling page {0}".format(1))


if __name__ == "__main__":
    spider = PrimarySchoolAreaSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()
