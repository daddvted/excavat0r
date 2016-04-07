# -*- coding: utf-8 -*-
# Spider for　成都市社保局-常见问题
from __future__ import unicode_literals
import re
import urllib
import mysql.connector
import random
import requests
from bs4 import BeautifulSoup

from engine.SpiderMan import SpiderMan


class CDSocialSecuritySpider(SpiderMan):
    def __init__(self, host):
        self.host = host
        self.question_url = []
        items = [
            "城镇职工基本医疗保险",
            "城乡居民基本医疗保险",
            "城镇职工基本养老保险",
            "城乡居民基本养老保险",
            "失业保险",
            "生育保险",
            "工伤保险",
        ]
        url = "http://%s/interactive/quesFile.jsp" % self.host
        self.http_headers["host"] = self.host

        for item in items:
            self.http_headers["User-Agent"] = random.choice(self.user_agents)

            post_data = {
                "ClassID": "0833040101",
            }
            post_data["infoType_p"] = item.encode("gbk")
            post_data["p"] = 1

            page = requests.post(url, headers=self.http_headers, data=post_data)
            page.encoding = 'gbk'
            tmp = page.content.decode('gbk')
            soup = BeautifulSoup(tmp, "html5lib")
            html = soup.find("p", class_="textCenter lineH34px").get_text()
            m = re.search(r'/([0-9]+)\s', html)
            if m:
                page_num = int(m.group(1))

            for n in range(1, page_num + 1):
                post_data["p"] = n
                page = requests.post(url, headers=self.http_headers, data=post_data)
                page.encoding = 'gbk'
                tmp = page.content.decode('gbk')
                soup = BeautifulSoup(tmp, "html5lib")
                html0 = soup.find("table", class_="tb1 tbico1 f14px").find_all("a")
                for h in html0:
                    self.question_url.append("http://%s%s" % (self.host, h.get("href")))

    def start2crawl(self):
        config = {
            'user': 'root',
            'password': 'hello',
            'host': '192.168.110.222',
            'port': '3306',
            'database': 'ai1',
            'raise_on_warnings': True,
        }
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        for url in self.question_url:
            print "processing %s" % url
            self.http_headers["User-Agent"] = random.choice(self.user_agents)
            self.http_headers["host"] = self.host

            page = requests.get(url, headers=self.http_headers)
            html = BeautifulSoup(page.text, "html5lib")
            html0 = html.find("div", class_="detail")
            question = html0.h1.string
            answer = html0.find("div", class_="details").get_text()
            answer = answer.strip()

            insert_stmt = (
                "INSERT INTO cd_social_security(question, answer) VALUES(%s, %s)"
            )
            data = (unicode(question), unicode(answer))
            cursor.execute(insert_stmt, data)
            conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    spider = CDSocialSecuritySpider("www.cdhrss.gov.cn")
    spider.start2crawl()
