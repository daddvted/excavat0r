"""
主城拟供应地块公告
URL: http://jyzx.cqgtfw.gov.cn/ngytd/ngytd.asp
"""
import urllib.request
import lxml.html
import mysql.connector
from service_api.Utils import fake_useragent


class LandAnnouncementSpider(object):
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
        template = "INSERT INTO landannouncement(location, land_use, area, allow_area, transfer_fee1, transfer_fee2, remark, end_time, url) " \
                   "VALUES (%(location)s, %(land_use)s, %(area)s, %(allow_area)s, %(transfer_fee1)s, %(transfer_fee2)s, %(remark)s, %(end_time)s, %(url)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    @staticmethod
    def prepare2crawl():
        url_template = "http://jyzx.cqgtfw.gov.cn/ngytd/ngytd.asp?Page={}"
        base_url = "http://jyzx.cqgtfw.gov.cn{}"

        for p in range(1, 30):
            print("------ Processing page {}".format(p))
            header = {
                "User-Agent": fake_useragent(),
                "Cookie": 'safedog-flow-item=68FF67A6B6FD8EB31DDBEC634E6D791A; ASPSESSIONIDACBRDBAR=NCBEMHBDKKIDLJBKGCAILHNM',
                "Host": "jyzx.cqgtfw.gov.cn",
                "Referer": "http://jyzx.cqgtfw.gov.cn/ngytd/ngytd.asp"

            }

            req = urllib.request.Request(url_template.format(p), headers=header, method="GET")
            resp = urllib.request.urlopen(req)

            print(resp.status)
            if resp.status == 200:
                # print(resp.read())
                # print(resp.read().decode("gbk"))
                result = resp.read().decode("gbk")
                html = lxml.html.fromstring(result)
                trs = html.xpath('//tr[@bgcolor="#ffe8e8"]')
                print(trs)
                for tr in trs:
                    tds = tr.xpath('.//td')
                    a = tds[1].xpath('./a')[0]
                    href = a.attrib["href"]
                    url = base_url.format(href.lstrip('.'))
                    location = a.text_content().strip()
                    data = {
                        "location": location,
                        "land_use": tds[2].text_content().strip(),
                        "area": tds[3].text_content().strip(),
                        "allow_area": tds[4].text_content().strip(),
                        "transfer_fee1": tds[5].text_content().strip(),
                        "transfer_fee2": tds[6].text_content().strip(),
                        "remark": tds[7].text_content().strip(),
                        "end_time": tds[8].text_content().strip(),
                        "url": url
                    }
                    print(data)
                    # self.save2db(data)
            else:
                print("Error processing page {}".format(p))
                break

            print("------ Finish page {}".format(p))

    def crawl(self, page):
        pass

    def final_crawl(self):
        pass

if __name__ == "__main__":
    spider = LandAnnouncementSpider()
    spider.prepare2crawl()

    spider.cursor.close()
    spider.conn.close()
