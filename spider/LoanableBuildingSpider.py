"""
成都市贷款楼盘查询
URL: http://www.chengdu.gov.cn/servicelist/xxjy04/
"""

import requests
import lxml.html
import mysql.connector


class LoanableBuildingSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.1.172',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }
    url = {
        "2016": "http://www.cdzfgjj.gov.cn/index.php?m=content&c=index&a=lists&catid=85",
        "2015": "http://www.cdzfgjj.gov.cn/index.php?m=content&c=index&a=lists&catid=84",
        "2014": "http://www.cdzfgjj.gov.cn/index.php?m=content&c=index&a=lists&catid=66",
        "2013": "http://www.cdzfgjj.gov.cn/index.php?m=content&c=index&a=lists&catid=65",
        "2012": "http://www.cdzfgjj.gov.cn/index.php?m=content&c=index&a=lists&catid=64",
    }

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def save2db(self, data):
        template = "INSERT INTO loanable_building(name, addr, developer, admin, type, update_month, year) " \
                   "VALUES (%(name)s, %(addr)s, %(developer)s, %(admin)s, %(type)s, %(update_month)s, %(year)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def crawl(self):
        print("====== Processing page {0} ======".format(1))

        for year in self.url.keys():
            browser = requests.get(self.url[year])

            if browser.status_code == 200:
                root = lxml.html.fromstring(browser.text)
                trs = root.xpath('//table[@class="table-det"]/tbody/tr')
                for tr in trs:
                    tds = tr.xpath('.//td')
                    data = {
                        "name": str(tds[1].text_content()),
                        "addr": str(tds[2].text_content()),
                        "developer": str(tds[3].text_content()),
                        "admin": str(tds[4].text_content()).strip('\r'),
                        "type": str(tds[5].text_content()),
                        "update_month": str(tds[6].text_content()),
                        "year": year
                    }
                    self.save2db(data)



            else:
                print("Error when crawling page {0}".format(link))


if __name__ == "__main__":
    spider = LoanableBuildingSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()
