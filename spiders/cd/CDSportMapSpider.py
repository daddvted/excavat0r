"""
成都体育实景地图
URL: http://ty.cd168.cn/
"""
import json
import re
import mysql.connector
import requests
from urllib.parse import urlencode
from service_api.Utils import fake_useragent


class CDSportMapSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service_cd',
        'raise_on_warnings': True,

    }

    def __init__(self):
        # Init mysql
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

        self.cookie = None
        self.area = {
            "1": "锦江区",
            "2": "青羊区",
            "3": "金牛区",
            "4": "武侯区",
            "5": "成华区",
            "6": "高新区",
            "7": "龙泉驿区",
            "8": "青白江区",
            "9": "新都区",
            "10": "温江区",
            "11": "都江堰市",
            "12": "彭州市",
            "13": "邛崃市",
            "14": "崇州市",
            "15": "金堂县",
            "16": "双流县",
            "17": "郫县",
            "18": "大邑县",
            "19": "蒲江县",
            "20": "新津县",
        }

        self.headers = {
            # "User-Agent": random.choice(self.USER_AGENTS),
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://ty.cd168.cn',
            'Referer': 'http://ty.cd168.cn/',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.cls = dict()

    def save2db(self, data):

        template = "INSERT INTO sportgoods(name, principal, tel, addr, website, area, class, latitude, longitude) "\
                   "VALUES (%(name)s, %(principal)s, %(tel)s, %(addr)s, %(website)s, %(area)s, %(class)s, %(latitude)s, %(longitude)s)"
        # template = "INSERT INTO fitnesspath(name, principal, tel, addr, website, area, latitude, longitude) "\
        #            "VALUES (%(name)s, %(principal)s, %(tel)s, %(addr)s, %(website)s, %(area)s, %(latitude)s, %(longitude)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def prepare2crawl(self):
        url = "http://ty.cd168.cn/Json/getClass/"

        data = {
            "categoryid": 8
        }
        self.headers["User-Agent"] = fake_useragent()
        browser = requests.post(url, headers=self.headers, data=urlencode(data))
        if browser.status_code == 200:
            tmp = json.loads(browser.text)
            for item in tmp:
                tmp = item["ItemName"].strip()
                self.cls[item["ID"]] = re.sub(r'\s+', '', tmp)

            self.crawl()
        else:
            print("Error getting class")

    def crawl(self):
        url = "http://ty.cd168.cn/Json/getPoint/"

        for k in self.cls.keys():
            print("++++++++++++++++ {} ++++++++++++++++".format(self.cls[k]))
        # for _ in range(1, 2):

            data = {
                # 行政区划: 0 - 所有区域
                "areaid": 0,
                # 1 - 公共场馆
                # 2 - 体育彩票
                # 3 - 体质监测
                # 4 - 健身路径
                # 5 - 健身会所
                # 6 - 学校场地
                # 7 - 体育培训
                # 8 - 体育用品
                "categoryid": 8,
                # 分类项目: 0 - 所有分类
                "classid": int(k),
                # "classid": 0,
            }
            self.headers["User-Agent"] = fake_useragent()
            browser = requests.post(url, headers=self.headers, data=urlencode(data))
            if browser.status_code == 200:
                result = json.loads(browser.text)
                print(result["Page"]["TotalCount"])
                total = int(result["Page"]["TotalPage"]) + 1
                for p in range(1, total):
                    print("------ {} ------".format(p))
                    data["pageindex"] = p
                    browser = requests.post(url, headers=self.headers, data=urlencode(data))
                    result = json.loads(browser.text)

                    points = result["Point"]
                    for point in points:
                        tmp = {
                            "name": point["PointName"],
                            "principal": point["Principal"],
                            "tel": point["Phone"],
                            "addr": point["Address"],
                            "website": point["WebSite"],
                            "area": self.area[str(point["AreaID"])],
                            "class": self.cls[k],
                            "latitude": str(point["Lat"]),
                            "longitude": str(point["Lon"])
                        }
                        self.save2db(tmp)
                        # print(tmp)

if __name__ == "__main__":
    spider = CDSportMapSpider()
    spider.prepare2crawl()

    spider.cursor.close()
    spider.conn.close()
