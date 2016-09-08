"""
疫苗接种点查询
URL: http://www.cqwsjsw.gov.cn/Html/1/jbyf/index.html
"""
import re
import random
import urllib.request
import lxml.html
import mysql.connector
from urllib.parse import quote, unquote


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

        self.USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MI NOTE LTE Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025489 Mobile Safari/533.1" \
            " MicroMessenger/6.3.13.49_r4080b63.740 NetType/cmnet Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 MicroMessenger/6.3.13 NetType/WIFI Language/zh_CN",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Shuame; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.1.1000 Chrome/39.0.2146.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13",
            "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8",
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)",
            "Googlebot/2.1 (http://www.googlebot.com/bot.html)",
            "Opera/9.20 (Windows NT 6.0; U; en)",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)",
            "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
        ]

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
                "User-Agent": random.choice(self.USER_AGENTS)
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
