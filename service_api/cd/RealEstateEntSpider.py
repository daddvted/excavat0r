"""
房地产企业
URL: http://www.cdcc.gov.cn/webNew/aspx/EnterpriseLst.aspx?st=%B7%BF%B5%D8%B2%FA%C6%F3%D2%B5&sn=&sz=&page=
抓取日期: 20160721
该爬虫也可爬取该页面其它企业类别
"""
import time
import random
import requests
import lxml.html
import mysql.connector
from service_api.Utils import fake_useragent


class ReligionSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }

    URL = "http://www.cdcc.gov.cn/webNew/aspx/EnterpriseLst.aspx?st=%B7%BF%B5%D8%B2%FA%C6%F3%D2%B5&sn=&sz=&page={}"
    BASE_URL = "http://www.cdcc.gov.cn/webNew/aspx/"

    def __init__(self):
        # Init mysql
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def save2db(self, data):

        template = "INSERT INTO real_estate_ent(name, addr, level, certificate_no) " \
                   "VALUES (%(name)s, %(addr)s, %(level)s, %(certificate_no)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    # 1st crawl, get total
    def crawl(self):
        for n in range(1, 137):
            print("------ Crawling page {} ------".format(n))
            url = self.URL.format(n)
            print(url)
            headers = {
                "User-Agent": fake_useragent()
            }
            browser = requests.get(url, headers=headers)

            if browser.status_code == 200:
                html = lxml.html.fromstring(browser.text)
                links = html.xpath('//div[@class="search_Newslistinn"]/ul/li/div/a')
                for link in links:
                    tmp_url = self.BASE_URL + link.attrib["href"]
                    self.crawl2(tmp_url)
            else:
                print("Error while crawling page {}".format(n))

            time.sleep(random.randint(1, 3))

    def crawl2(self, url):
        print("processing url: {}".format(url))
        headers = {
            "User-Agent": fake_useragent()
        }
        browser = requests.get(url, headers=headers)
        if browser.status_code == 200:
            html = lxml.html.fromstring(browser.text)
            data = {
                "name": html.xpath('//span[@id="lbUnitName"]')[0].text_content().strip(),
                "addr": html.xpath('//span[@id="lbAddress"]')[0].text_content().strip(),
                "level": html.xpath('//span[@id="lbAptGrade"]')[0].text_content().strip(),
                "certificate_no": html.xpath('//span[@id="lbcertificateNo"]')[0].text_content().strip(),
            }
            self.save2db(data)
        else:
            print("Error while crawling page {}".format(url))

if __name__ == "__main__":
    spider = ReligionSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()

