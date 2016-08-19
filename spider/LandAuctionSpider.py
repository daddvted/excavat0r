"""
土地拍卖结果公示
URL: http://www.cdggzy.com:8112/two/pmjg.html
"""
import re
import json
import random
import requests
import lxml.html
import mysql.connector
from urllib.parse import urlencode
from spider.LarvaSpider import Larva


class LandAuctionSpider(Larva):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service_cd',
        'raise_on_warnings': True,

    }
    base_url = "http://www.cdggzy.com:8112"

    def __init__(self):
        # Init mysql
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

        self.headers = {
            # "User-Agent": random.choice(self.USER_AGENTS),
            # 'Accept': 'application/json, text/javascript, */*',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
            # 'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Origin': 'http://ty.cd168.cn',
            # 'Referer': 'http://ty.cd168.cn/',
            # 'X-Requested-With': 'XMLHttpRequest',
        }

    def save2db(self, data):

        template = "INSERT INTO sportgoods(name, principal, tel, addr, website, area, class, latitude, longitude) "\
                   "VALUES (%(name)s, %(principal)s, %(tel)s, %(addr)s, %(website)s, %(area)s, %(class)s, %(latitude)s, %(longitude)s)"
        # template = "INSERT INTO fitnesspath(name, principal, tel, addr, website, area, latitude, longitude) "\
        #            "VALUES (%(name)s, %(principal)s, %(tel)s, %(addr)s, %(website)s, %(area)s, %(latitude)s, %(longitude)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def prepare2crawl(self):
        url = "http://www.cdggzy.com:8112/two/pmjg_Detail.aspx"
        for p in range(1, 2):

            data = {
                '__VIEWSTATE': '/wEPDwULLTExNzkxNTY4MjEPZBYCAgMPZBYEAgEPFgIeC18hSXRlbUNvdW50Ag8WHmYPZBYCZg8VAwoyMDE2LzA4LzE5BjMwNjU1NTHmi43ljZbkvJrmiJDkuqTnu5PmnpzkuIDop4jooagoMjAxNuW5tDA45pyIMTnml6UpZAIBD2QWAmYPFQMKMjAxNi8wOC8wOQYyOTEyODAx5ouN5Y2W5Lya5oiQ5Lqk57uT5p6c5LiA6KeI6KGoKDIwMTblubQwOOaciDA55pelKWQCAg9kFgJmDxUDCjIwMTYvMDgvMDQGMjkwNDQ5MeaLjeWNluS8muaIkOS6pOe7k+aenOS4gOiniOihqCgyMDE25bm0MDjmnIgwNOaXpSlkAgMPZBYCZg8VAwoyMDE2LzA3LzI3BjI4MjkyMDHmi43ljZbkvJrmiJDkuqTnu5PmnpzkuIDop4jooagoMjAxNuW5tDA35pyIMjfml6UpZAIED2QWAmYPFQMKMjAxNi8wNy8yMQYyNzY3OTAx5ouN5Y2W5Lya5oiQ5Lqk57uT5p6c5LiA6KeI6KGoKDIwMTblubQwN+aciDIx5pelKWQCBQ9kFgJmDxUDCjIwMTYvMDcvMTMGMjcwMjMwMeaLjeWNluS8muaIkOS6pOe7k+aenOS4gOiniOihqCgyMDE25bm0MDfmnIgxM+aXpSlkAgYPZBYCZg8VAwoyMDE2LzA3LzA2BjI2NjY1MzHmi43ljZbkvJrmiJDkuqTnu5PmnpzkuIDop4jooagoMjAxNuW5tDA35pyIMDbml6UpZAIHD2QWAmYPFQMKMjAxNi8wNi8yOQYyNTkxMTMx5ouN5Y2W5Lya5oiQ5Lqk57uT5p6c5LiA6KeI6KGoKDIwMTblubQwNuaciDI55pelKWQCCA9kFgJmDxUDCjIwMTYvMDYvMjEGMjUyNzEzMeaLjeWNluS8muaIkOS6pOe7k+aenOS4gOiniOihqCgyMDE25bm0MDbmnIgyMeaXpSlkAgkPZBYCZg8VAwoyMDE2LzA2LzE2BjI0ODE5OTHmi43ljZbkvJrmiJDkuqTnu5PmnpzkuIDop4jooagoMjAxNuW5tDA25pyIMTbml6UpZAIKD2QWAmYPFQMKMjAxNi8wNi8xNAYyNDM1MjEx5ouN5Y2W5Lya5oiQ5Lqk57uT5p6c5LiA6KeI6KGoKDIwMTblubQwNuaciDE05pelKWQCCw9kFgJmDxUDCjIwMTYvMDYvMDEGMjM2MTQxMeaLjeWNluS8muaIkOS6pOe7k+aenOS4gOiniOihqCgyMDE25bm0MDbmnIgwMeaXpSlkAgwPZBYCZg8VAwoyMDE2LzA1LzMxBjIzNTM0NTHmi43ljZbkvJrmiJDkuqTnu5PmnpzkuIDop4jooagoMjAxNuW5tDA15pyIMzHml6UpZAIND2QWAmYPFQMKMjAxNi8wNS8yNQYyMzM2MjUx5ouN5Y2W5Lya5oiQ5Lqk57uT5p6c5LiA6KeI6KGoKDIwMTblubQwNeaciDI15pelKWQCDg9kFgJmDxUDCjIwMTYvMDUvMTkGMjMwNTM1MeaLjeWNluS8muaIkOS6pOe7k+aenOS4gOiniOihqCgyMDE25bm0MDXmnIgxOeaXpSlkAgMPDxYEHgtSZWNvcmRjb3VudAKpAR4QQ3VycmVudFBhZ2VJbmRleAIBZGRknBpMzCh1lVAb0hQ+KYqaC3XY/ObAUBQzQyX+ubYfCdU=',
                '__EVENTTARGET': 'Pager',
                '__EVENTARGUMENT': 1,
            }
            self.headers["User-Agent"] = random.choice(self.USER_AGENTS)
            browser = requests.post(url, headers=self.headers, data=urlencode(data))
            if browser.status_code == 200:
                root = lxml.html.fromstring(browser.text)
                lis = root.xpath('//div[@class="list1"]/li')
                for li in lis:
                    date = li.xpath('//span')[0].text_content().strip()
                    date = date.replace('/', '-')

                    url = li.xpath('//a')[0].attrib["href"]
                    url = url.replace('..', '')

                    self.crawl(date, self.base_url + url)

            else:
                print("Error crawling page {}".format(p))

    def crawl(self, date, url):
        # for _ in range(1, 2):

            self.headers["User-Agent"] = random.choice(self.USER_AGENTS)
            browser = requests.get(url, headers=self.headers)
            if browser.status_code == 200:
                print(browser.text)



if __name__ == "__main__":
    spider = LandAuctionSpider()
    spider.prepare2crawl()

    spider.cursor.close()
    spider.conn.close()

