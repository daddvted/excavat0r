"""
小升初学校查询
URL: http://www.cdzsks.com/school/search
"""
import json
import requests
from spider.Utils import fake_useragent


class HighSchoolSpider(object):

    def __init__(self):
        self.login_url = "http://www.cdzsks.com/home/login"

    def login(self):

        data = {
            "UserID": "360281198903120044",
            "loginPassword": "vickyWW520",
        }

        headers = {
            "User-Agent": fake_useragent()
        }

        response = requests.post(self.login_url, headers=headers, data=json.dumps(data))

        print(response.cookies.get_dict())

if __name__ == "__main__":
    spider = HighSchoolSpider()
    spider.login()


