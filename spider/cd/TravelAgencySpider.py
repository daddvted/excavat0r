"""
四川旅行社列表
URL: http://www.tsichuan.com/travellist.htm?type=&region=510100&pageNo=1
爬取日期: 2016-7-8
爬取页面: 1 - 41
"""
import sys
import time
import random
import requests
import lxml.html
from bs4 import BeautifulSoup
import mysql.connector


class TravelAgencySpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MI NOTE LTE Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025489 Mobile Safari/533.1 MicroMessenger/6.3.13.49_r4080b63.740 NetType/cmnet Language/zh_CN",
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

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

        self.headers = {}

    def save2db(self, data):
        template = "INSERT INTO travel_agency(name, license, type, addr, tel, zip, email, website, route) " \
                   "VALUES (%(name)s, %(license)s, %(type)s, %(addr)s, %(tel)s, %(zip)s, %(email)s, %(website)s, %(route)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def crawl(self, start):
        base_url = "http://www.tsichuan.com/{0}"
        url = "http://www.tsichuan.com/travellist.htm?type=&region=510100&pageNo={0}"
        for m in range(start, 41):
            print("====== Processing page {0} ======".format(m))
            browser = requests.post(url.format(m))
            if browser.status_code == 200:
                root = lxml.html.fromstring(browser.text)
                links = root.xpath('//div[@class="wzsc_lxs_list"]/dl/dd/h3/a')
                for link in links:
                    new_url = base_url.format(link.attrib["href"])
                    self.crawl2(new_url)
            else:
                print("Error when crawling page {0}".format(m))

    def crawl2(self, url):
        print("processing: {0}".format(url))
        self.headers["User-Agent"] = random.choice(self.USER_AGENTS)
        browser = requests.get(url, headers=self.headers)
        if browser.status_code == 200:
            # root = lxml.html.fromstring(browser.text)
            # lis = root.xpath('//ul[@class="wzsc_bgjd_cs_jbxx"]/li')

            root = BeautifulSoup(browser.text, 'lxml')
            lis = root.find('ul', class_="wzsc_bgjd_cs_jbxx").find_all("li")

            tp = lis[2].contents[1].strip('\r\n').replace('\t', '').replace(' ', '').strip('\r\n').replace('\r\n', ',')
            link = lis[7].find('a')
            website = link.get("href") if link else "#"
            route = root.find_all("div", class_="wzsc_bgjd_cs_p contoxt")[1].text.strip()

            data = {
                "name": str(lis[0].contents[1]) if len(lis[0].contents) > 1 else "",
                "license": str(lis[1].contents[1]) if len(lis[1].contents) > 1 else "",
                "type": tp,
                "addr": str(lis[3].contents[1]) if len(lis[3].contents) > 1 else "",
                "tel": str(lis[4].contents[1]) if len(lis[4].contents) > 1 else "",
                "zip": str(lis[5].contents[1]) if len(lis[5].contents) > 1 else "",
                "email": str(lis[6].contents[1]) if len(lis[6].contents) > 1 else "",
                "website": website,
                "route": route
            }
            self.save2db(data)

        else:
            print("Error when processing url: {0}".format(url))
        time.sleep(random.randint(1, 3))


if __name__ == "__main__":
    start = sys.argv[1]
    spider = TravelAgencySpider()
    spider.crawl(int(start))

    spider.cursor.close()
    spider.conn.close()
