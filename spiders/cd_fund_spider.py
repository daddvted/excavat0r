# -*- coding: utf-8 -*-
# Spider for　成都市住房公积金管理中心－热点问题
import random

import mysql.connector
import requests
from bs4 import BeautifulSoup

from engine.SpiderMan import SpiderMan


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
            print("processing %s" % q
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


