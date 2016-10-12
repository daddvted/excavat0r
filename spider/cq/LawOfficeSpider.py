"""
疫苗接种点查询
URL: http://www.cqwsjsw.gov.cn/Html/1/jbyf/index.html
"""
import re
import urllib.request
import lxml.html
import mysql.connector
from spider.Utils import fake_useragent


class LawOfficeSpider(object):
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

        self.url_template = "http://118.125.243.115/search/lawyers.aspx?key=&lawfirm=&lawyer=&E=&page={}"
        self.base_url = "http://118.125.243.115/search/{}"

    def save2db(self, data):
        template = "INSERT INTO lawyer(name, license, type, office, expertise, education, area, link) " \
                   "VALUES (%(name)s, %(license)s, %(type)s, %(office)s, %(expertise)s, %(education)s, %(area)s, %(link)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def prepare2crawl(self):
        for p in range(1, 1435):
            print("------ Processing page {}".format(p))
            url = self.url_template.format(p)

            header = {
                "User-Agent": fake_useragent()
            }

            req = urllib.request.Request(url, headers=header, method="GET")
            resp = urllib.request.urlopen(req)

            if resp.status == 200:
                html = lxml.html.fromstring(resp.read().decode("utf-8"))

                divs = html.xpath('//div[@class="content_left_bg"]/div')
                if len(divs):
                    for n in range(2, len(divs)):
                        tds = divs[n].xpath('.//td')
                        href = tds[2].xpath('./a')[0].attrib["href"]
                        link = self.base_url.format(href)
                        data = {
                            "name": re.sub('律师', '', tds[2].xpath('./a')[0].text_content()),
                            "license": re.split(r'[:|：]', tds[5].text_content())[1],
                            "type": re.split(r'[:|：]', tds[6].text_content())[1],
                            "office": tds[7].text_content().strip(),
                            "expertise": re.split(r'[:|：]', tds[8].text_content())[1],
                            "education": re.split(r'[:|：]', tds[9].text_content())[1],
                            "area": tds[4].text_content().strip(),
                            "link": link,
                        }
                        self.save2db(data)
            else:
                print("Error processing page {}".format(p))

    def crawl(self):
        pass

    def final_crawl(self):
        pass


if __name__ == "__main__":
    spider = LawOfficeSpider()
    spider.prepare2crawl()

    spider.cursor.close()
    spider.conn.close()
