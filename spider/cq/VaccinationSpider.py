"""
疫苗接种点查询
URL: http://www.cqwsjsw.gov.cn/Html/1/jbyf/index.html
"""
import re
import random
import urllib.request
import lxml.html
import mysql.connector

from spider.Larva import Larva


class VaccinationSpider(Larva):
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
            "User-Agent": random.choice(self.USER_AGENTS)
        }

        self.domain = "http://www.cqwsjsw.gov.cn{}"
        self.url_list = []
        self.area = {
            "1": "巴南区",
            "2": "北碚区",
            "3": "北部新区",
            "4": "璧山区",
            "5": "长寿区",
            "6": "城口县",
            "7": "大渡口区",
            "8": "大足区",
            "9": "垫江县",
            "10": "丰都县",
            "11": "奉节县",
            "12": "涪陵区",
            "13": "合川区",
            "14": "江北区",
            "15": "江津区",
            "16": "九龙坡区",
            "17": "开县",
            "18": "梁平县",
            "19": "南岸区",
            "20": "南川区",
            "21": "彭水苗族土家族自治县",
            "22": "綦江区",
            "23": "黔江区",
            "24": "荣昌区",
            "25": "沙坪坝区",
            "26": "石柱土家族自治县",
            "27": "铜梁区",
            "28": "潼南区",
            "29": "万盛经开区",
            "30": "万州区",
            "31": "巫山县",
            "32": "巫溪县",
            "33": "武隆县",
            "34": "秀山县",
            "35": "永川区",
            "36": "酉阳县",
            "37": "渝北区",
            "38": "渝中区",
            "39": "云阳县",
            "40": "忠县",
        }
        self.current_area = ""
        self.current_area_id = ""
        self.url_template = "http://www.cqwsjsw.gov.cn/wsfw/jbyf.aspx?fla=sel&name=&Address=&WardId={}&pageNo={}"

    def save2db(self, data):
        template = "INSERT INTO vaccination(name, addr, area, tel, time) " \
                   "VALUES (%(name)s, %(addr)s, %(area)s, %(tel)s, %(time)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def prepare2crawl(self):
        for k in self.area.keys():
            self.url_list = []
            self.current_area = self.area[k]
            self.current_area_id = k
            print("------------- {} -------------".format(self.area[k]))
            print("Processing page 1")
            url = self.url_template.format(k, 1)
            req = urllib.request.Request(url, headers=self.header, method="GET")
            resp = urllib.request.urlopen(req)

            if resp.status == 200:
                result = resp.read().decode("gbk")
                links = lxml.html.iterlinks(result)
                for link in links:
                    if re.match(r'/wsfw/jbyfshow\.aspx\?id=[\d+]', link[2]):
                        self.url_list.append(link[2])

                html = lxml.html.fromstring(result)
                total_page = html.xpath('//div[@class="pages-nav"]/span/font[2]')[0].text_content()

                self.crawl(int(total_page))

            else:
                print("Error getting class")

    def crawl(self, page):
        for p in range(2, page + 1):
            print("Processing page {}".format(p))
            url = self.url_template.format(self.current_area_id, p)

            req = urllib.request.Request(url, headers=self.header, method="GET")
            resp = urllib.request.urlopen(req)

            if resp.status == 200:
                result = resp.read().decode("gbk")
                links = lxml.html.iterlinks(result)
                for link in links:
                    if re.match(r'/wsfw/jbyfshow\.aspx\?id=[\d+]', link[2]):
                        self.url_list.append(link[2])
            else:
                print("Error processing page {}".format(p))

        self.final_crawl()

    def final_crawl(self):
        print("Length of url_list: {}".format(len(self.url_list)))
        for url in self.url_list:
            url = self.domain.format(url)

            req = urllib.request.Request(url, headers=self.header, method="GET")
            resp = urllib.request.urlopen(req)
            html = lxml.html.fromstring(resp.read().decode("gbk"))
            ps = html.xpath('//span[@id="yf_content"]/p')

            data = {
                "name": ps[0].text_content().split('：')[1],
                "addr": ps[2].text_content().split('：')[1],
                "area": self.current_area,
                "tel": ps[1].text_content().split('：')[1],
                "time": ps[3].text_content().split('：')[1],
            }
            # print(data)
            self.save2db(data)

if __name__ == "__main__":
    spider = VaccinationSpider()
    spider.prepare2crawl()

    spider.cursor.close()
    spider.conn.close()
