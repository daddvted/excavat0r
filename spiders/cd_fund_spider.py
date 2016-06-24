import random

import mysql.connector
import requests
from bs4 import BeautifulSoup

class SpiderMan:


    user_agents = [
        "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MI NOTE LTE Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025489 Mobile Safari/533.1 MicroMessenger/6.3.13.49_r4080b63.740 NetType/cmnet Language/zh_CN",
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
        "Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)",
        "Googlebot/2.1 (http://www.googlebot.com/bot.html)",
        "Opera/9.20 (Windows NT 6.0; U; en)",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)",
    ]
    http_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
    }

    def _360wenda(self, kw):
        url = 'http://wenda.so.com/search/?q=' + kw
        self.http_headers["host"] = 'wenda.so.com'
        self.http_headers["User-Agent"] = random.choice(self.user_agents)
        print(self.http_headers)
        page = requests.get(url, headers=self.http_headers)
        page.encoding = 'utf-8'
        soup = BeautifulSoup(page.text, "html5lib")
        html = soup.find_all("ul", class_="qa-list")
        return html

    def _zhidao(self, kw):
        url = 'http://zhidao.baidu.com/search?word=' + kw
        self.http_headers["host"] = 'zhidao.baidu.com'
        self.http_headers["User-Agent"] = random.choice(self.user_agents)
        page = requests.get(url, headers=self.http_headers)
        page.encoding = 'gbk'
        tmp = page.content.decode('gbk')
        soup = BeautifulSoup(tmp, "html5lib")
        # html = soup.find("dl", class_="dl")
        html = soup.find(id="wgt-list")
        return html

    def start2crawl(self, kw, site):
        # site:
        # 0 - 360问答
        # 1 - 百度知道
        pass


class CDFundSpider(SpiderMan):
    def __init__(self, host):
        self.host = host
        url = "http://%s/index.php?m=content&c=index&a=lists&catid=55" % host
        self.http_headers["User-Agent"] = random.choice(self.user_agents)
        self.http_headers["host"] = self.host
        page = requests.get(url, headers=self.http_headers)
        page.encoding = 'utf-8'
        soup = BeautifulSoup(page.text, "html5lib")
        html = soup.find(id="tab-q").find_all("a")
        self.content_url = []
        for a in html:
            self.content_url.append("http://%s/%s" % (self.host, a.get("href")))

    def start2crawl(self):
        all_question_url = []
        for url in self.content_url:
            page = requests.get(url, headers=self.http_headers)
            page.encoding = 'utf-8'
            soap = BeautifulSoup(page.text, "html5lib")
            html0 = soap.find("div", class_="page")
            if html0:
                html1 = html0.find_all("a", class_='num')
                for s in html1:
                    all_question_url.append("http://%s/%s" % (self.host, s.get("href")))

            else:
                all_question_url.append(url)
        final_urls = list(set(all_question_url))

        self.http_headers["User-Agent"] = random.choice(self.user_agents)
        self.http_headers["host"] = self.host
        question_urls = []
        for url in final_urls:
            page = requests.get(url, headers=self.http_headers)
            page.encoding = "utf-8"
            soap = BeautifulSoup(page.text, "html5lib")
            html0 = soap.find("div", class_="qa-list").ul.find_all("li")
            for html in html0:
                question_urls.append("http://%s/%s" % (self.host, html.a.get("href")))

        config = {
            'user': 'qa',
            'password': 'qa',
            'host': '192.168.110.222',
            'port': '3306',
            'database': 'qa',
            'raise_on_warnings': True,
        }
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        for q in question_urls:
            print("processing %s" % q)
            self.http_headers["User-Agent"] = random.choice(self.user_agents)
            self.http_headers["host"] = self.host
            page = requests.get(q, headers=self.http_headers)
            soap = BeautifulSoup(page.text, "html5lib")
            html0 = soap.find("div", "w-main")
            question = html0.find("div", "art-title").h1.string
            answer = html0.find("div", "art-content").get_text()

            insert_stmt = (
                "INSERT INTO cd_accumulation_fund(question, answer) VALUES(%s, %s)"
            )
            data = (unicode(question), unicode(answer))
            cursor.execute(insert_stmt, data)
            conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    spider = CDFundSpider("www.cdzfgjj.gov.cn")
    spider.start2crawl()


