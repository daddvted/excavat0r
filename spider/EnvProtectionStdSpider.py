"""
环境保护部 - 国家环境保护标准
URL: http://datacenter.mep.gov.cn/trs/query.action
"""
import time
import random
import requests
import lxml.html
import mysql.connector


class EnvProtectionStdSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }
    url = "http://datacenter.mep.gov.cn/trs/query.action"

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

        self.form_data = {
            "docsource": "all"
        }

    def save2db(self, data):
        # template = "INSERT INTO env_protection_std(std_no, std_name, std_name_en, std_release_time, " \
        #         "std_impl_time, std_digest, std_link) VALUES ('{std_no}', '{std_name}', '{std_name_en}'," \
        #         " '{std_release_time}', '{std_impl_time}', '{std_digest}', '{std_link}')"

        template = ("INSERT INTO env_protection_std "
                    "(std_no, std_name, std_name_en, std_release_time, std_impl_time, std_digest, std_link) "
                    "VALUES (%(std_no)s, %(std_name)s, %(std_name_en)s, %(std_release_time)s, %(std_impl_time)s, %(std_digest)s, %(std_link)s)")
        # sql = template.format(**data)
        self.cursor.execute(template, data)
        self.conn.commit()

    def crawl(self):
        for m in range(2, 45):
            print("====== Processing page {0} ======".format(m))
            self.form_data["page.pageNo"] = m
            browser = requests.post(self.url, data=self.form_data)

            if browser.status_code == 200:
                root = lxml.html.fromstring(browser.text)
                divs = root.xpath('//*[@style="display: none;"]')

                for div in divs:
                    trs = div.xpath('.//tr')
                    data = {
                        "std_no": trs[0].xpath('./td[2]')[0].text_content().strip(),
                        "std_name": trs[1].xpath('./td[2]')[0].text_content().strip(),
                        "std_name_en": trs[2].xpath('./td[2]')[0].text_content().strip(),
                        "std_release_time": trs[3].xpath('./td[2]')[0].text_content().strip(),
                        "std_impl_time": trs[4].xpath('./td[2]')[0].text_content().strip(),
                        "std_digest": trs[5].xpath('./td[2]')[0].text_content().strip(),
                        "std_link": trs[6].xpath('./td[2]/a')[0].attrib["href"],
                    }
                    self.save2db(data)
            else:
                print("Error when crawling page {0}".format(m))

            time.sleep(random.randint(2, 6))


if __name__ == "__main__":
    spider = EnvProtectionStdSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()
