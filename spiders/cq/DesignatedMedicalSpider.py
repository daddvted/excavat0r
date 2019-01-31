"""
工伤定点医疗机构查询
URL: http://ggfw.cqhrss.gov.cn/QueryBLH_mainSmXz.do?code=033
"""
import json
import urllib.request
import mysql.connector
from urllib.parse import urlencode


class DesignatedMedicalSpider(object):
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

        self.cookie = None
        self.area = {"5000000300": "市本级", "5001010300": "万州区", "5001140300": "黔江区", "5001020300": "涪陵区", "5001030300": "渝中区", "5001040300": "大渡口区", "5001050300": "江北区", "5001060300": "沙坪坝区", "5001070300": "九龙坡区", "5001080300": "南岸区",
                     "5001090300": "北碚区", "5001120300": "渝北区", "5001130300": "巴南区", "5001160300": "江津区", "5001170300": "合川区", "5001180300": "永川区", "5001150300": "长寿区", "5002220300": "綦江区", "5002230300": "潼南区", "5002240300": "铜梁区",
                     "5002250300": "大足区", "5002260300": "荣昌区", "5002270300": "璧山区", "5002280300": "梁平县", "5002290300": "城口县", "5001190300": "南川区", "5002300300": "丰都县", "5002310300": "垫江县", "5002320300": "武隆县", "5002330300": "忠县",
                     "5002340300": "开县", "5002350300": "云阳县", "5002360300": "奉节县", "5002370300": "巫山县", "5002380300": "巫溪县", "5002400300": "石柱县", "5002410300": "秀山县", "5002420300": "酉阳县", "5002430300": "彭水县", "5009030300": "北部新区",
                     "5001430300": "万盛区"}

        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        self.tp = "药店"
        self.data = {
            "code": "033",
            "afwjglx": self.tp,
            "pageSize": "1000"
        }

    def save2db(self, data):

        # template = "INSERT INTO designatedmedical(area, name, type, level, tel, addr) " \
        #            "VALUES (%(area)s, %(name)s, %(type)s, %(level)s, %(tel)s, %(addr)s)"
        template = "INSERT INTO designatedmedical(area, name, type, special, tel, addr) " \
                   "VALUES (%(area)s, %(name)s, %(type)s, %(special)s, %(tel)s, %(addr)s)"
        self.cursor.execute(template, data)
        self.conn.commit()

    def prepare2crawl(self):
        url = "http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_querySmXz.do"

        for k in self.area.keys():
            print("------------- {} -------------".format(self.area[k]))
            self.data["ajbjg"] = k
            data = urlencode(self.data).encode('ascii')
            req = urllib.request.Request(url, data=data, headers=self.headers, method="POST")
            resp = urllib.request.urlopen(req)

            if resp.status == 200:
                result = json.loads(resp.read().decode("utf-8"))
                for item in result["result"]:
                    data = {
                        "area": self.area[k],
                        "name": item["fwjgmc"] if "fwjgmc" in item else "",
                        "type": self.tp,
                        "special": item["yydj"] if "yydj" in item else "",
                        "tel": item["lxdh"] if "lxdh" in item else "",
                        "addr": item["dz"] if "dz" in item else ""
                    }
                    self.save2db(data)

            else:
                print("Error getting class")

    def crawl(self):
        pass

if __name__ == "__main__":
    spider = DesignatedMedicalSpider()
    spider.prepare2crawl()

    spider.cursor.close()
    spider.conn.close()
