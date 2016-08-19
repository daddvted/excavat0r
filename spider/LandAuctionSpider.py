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
    post_url = "http://www.cdggzy.com:8112/two/pmjg_Detail.aspx"

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

        template = "INSERT INTO landauction(no, addr, area, price, winner, date) "\
                   "VALUES (%(no)s, %(addr)s, %(area)s, %(price)s, %(winner)s, %(date)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def prepare2crawl(self):
        for p in range(3, 13):
            print("----------- Crawling page {} -----------".format(p))

            data = {
                '__VIEWSTATE': '/wEPDwULLTExNzkxNTY4MjEPZBYCAgMPZBYEAgEPFgIeC18hSXRlbUNvdW50Ag8WHmYPZBYCZg8VAwoyMDE2LzA4LzE5BjMwNjU1NTHmi43ljZbkvJrmiJDkuqTnu5PmnpzkuIDop4jooagoMjAxNuW5tDA45pyIMTnml6UpZAIBD2QWAmYPFQMKMjAxNi8wOC8wOQYyOTEyODAx5ouN5Y2W5Lya5oiQ5Lqk57uT5p6c5LiA6KeI6KGoKDIwMTblubQwOOaciDA55pelKWQCAg9kFgJmDxUDCjIwMTYvMDgvMDQGMjkwNDQ5MeaLjeWNluS8muaIkOS6pOe7k+aenOS4gOiniOihqCgyMDE25bm0MDjmnIgwNOaXpSlkAgMPZBYCZg8VAwoyMDE2LzA3LzI3BjI4MjkyMDHmi43ljZbkvJrmiJDkuqTnu5PmnpzkuIDop4jooagoMjAxNuW5tDA35pyIMjfml6UpZAIED2QWAmYPFQMKMjAxNi8wNy8yMQYyNzY3OTAx5ouN5Y2W5Lya5oiQ5Lqk57uT5p6c5LiA6KeI6KGoKDIwMTblubQwN+aciDIx5pelKWQCBQ9kFgJmDxUDCjIwMTYvMDcvMTMGMjcwMjMwMeaLjeWNluS8muaIkOS6pOe7k+aenOS4gOiniOihqCgyMDE25bm0MDfmnIgxM+aXpSlkAgYPZBYCZg8VAwoyMDE2LzA3LzA2BjI2NjY1MzHmi43ljZbkvJrmiJDkuqTnu5PmnpzkuIDop4jooagoMjAxNuW5tDA35pyIMDbml6UpZAIHD2QWAmYPFQMKMjAxNi8wNi8yOQYyNTkxMTMx5ouN5Y2W5Lya5oiQ5Lqk57uT5p6c5LiA6KeI6KGoKDIwMTblubQwNuaciDI55pelKWQCCA9kFgJmDxUDCjIwMTYvMDYvMjEGMjUyNzEzMeaLjeWNluS8muaIkOS6pOe7k+aenOS4gOiniOihqCgyMDE25bm0MDbmnIgyMeaXpSlkAgkPZBYCZg8VAwoyMDE2LzA2LzE2BjI0ODE5OTHmi43ljZbkvJrmiJDkuqTnu5PmnpzkuIDop4jooagoMjAxNuW5tDA25pyIMTbml6UpZAIKD2QWAmYPFQMKMjAxNi8wNi8xNAYyNDM1MjEx5ouN5Y2W5Lya5oiQ5Lqk57uT5p6c5LiA6KeI6KGoKDIwMTblubQwNuaciDE05pelKWQCCw9kFgJmDxUDCjIwMTYvMDYvMDEGMjM2MTQxMeaLjeWNluS8muaIkOS6pOe7k+aenOS4gOiniOihqCgyMDE25bm0MDbmnIgwMeaXpSlkAgwPZBYCZg8VAwoyMDE2LzA1LzMxBjIzNTM0NTHmi43ljZbkvJrmiJDkuqTnu5PmnpzkuIDop4jooagoMjAxNuW5tDA15pyIMzHml6UpZAIND2QWAmYPFQMKMjAxNi8wNS8yNQYyMzM2MjUx5ouN5Y2W5Lya5oiQ5Lqk57uT5p6c5LiA6KeI6KGoKDIwMTblubQwNeaciDI15pelKWQCDg9kFgJmDxUDCjIwMTYvMDUvMTkGMjMwNTM1MeaLjeWNluS8muaIkOS6pOe7k+aenOS4gOiniOihqCgyMDE25bm0MDXmnIgxOeaXpSlkAgMPDxYEHgtSZWNvcmRjb3VudAKpAR4QQ3VycmVudFBhZ2VJbmRleAIBZGRknBpMzCh1lVAb0hQ+KYqaC3XY/ObAUBQzQyX+ubYfCdU=',
                '__EVENTTARGET': 'Pager',
                '__EVENTARGUMENT': 1,
            }
            self.headers["User-Agent"] = random.choice(self.USER_AGENTS)
            browser = requests.post(self.post_url, headers=self.headers, data=urlencode(data))
            if browser.status_code == 200:
                html = lxml.html.fromstring(browser.text)
                lis = html.xpath('//div[@class="list1"]/li')
                for li in lis:
                    href = li.xpath('./a')[0].attrib["href"]
                    url = href.replace('..', '')

                    self.crawl(self.base_url + url)
            else:
                print("Error crawling page {}".format(p))

    def crawl(self, url):
        self.headers["User-Agent"] = random.choice(self.USER_AGENTS)
        browser = requests.get(url, headers=self.headers)
        if browser.status_code == 200:
            html = lxml.html.fromstring(browser.text)
            src = html.xpath('//iframe[@id="wzzwInfo"]')[0].attrib["src"]
            url = self.base_url + src.replace('..', '')
            print(url)
            m = re.search(r'\d\d\d\d-\d\d-\d\d', url)
            date = m.group(0)


            browser = requests.get(url, headers=self.headers)
            html = lxml.html.fromstring(browser.text)
            trs = html.xpath('//table/tr')
            for tr in trs:
                tds = tr.xpath('.//td')
                if len(tds):
                    data = {
                        "no": tds[1].text_content().strip(),
                        "addr": tds[2].text_content().strip(),
                        "area": tds[3].text_content().strip(),
                        "price": tds[4].text_content().strip(),
                        "winner": tds[5].text_content().strip(),
                        "date": date,
                    }
                    self.save2db(data)

if __name__ == "__main__":
    spider = LandAuctionSpider()
    spider.prepare2crawl()

    spider.cursor.close()
    spider.conn.close()

