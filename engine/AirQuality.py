import re
import json
import random
import tornado.web
import tornado.gen
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPError
from tornado.httpclient import AsyncHTTPClient
from bs4 import BeautifulSoup
from .Handlers import Kernel


class AirQualityHandler(Kernel):
    url = "http://www.cdepb.gov.cn/cdepbws/Web/gov/airquality.aspx"

    @tornado.gen.coroutine
    def get(self):

        headers = {
            "User-Agent": random.choice(self.USER_AGENTS)
        }
        aqi = {}
        # aqi = {
        #           "main_index": "130",
        #           "main_pollution": "首要污染物：PM2.5",
        #           "aqi_level": "轻度污染",
        #           "time": ""
        #           "pollutions": [
        #               {
        #                   "pollution": "XXXXXX",
        #                   "index": "3"
        #               },
        #               {
        #                   "pollution": "XXXXXX",
        #                   "index": "37"
        #               }
        #           ]
        # }

        try:
            browser = AsyncHTTPClient()
            request = HTTPRequest(self.url, method="GET", headers=headers)
            response = yield browser.fetch(request)
            result = response.body
            html = BeautifulSoup(result.decode(), "html5lib")
            city_aqi_div = html.find("div", class_="CityAQI")

            main_index = city_aqi_div.find(id="ContentBody_AqiData").string
            aqi_level = city_aqi_div.find(id="ContentBody_StdName").string
            main_pollution = city_aqi_div.find(id="ContentBody_FirstPoll").string
            update_time = city_aqi_div.find(id="ContentBody_AQITime").string
            matches = re.findall('\d+', str(update_time))
            update_time = "{}-{}-{} {}".format(*matches)

            aqi["main_index"] = main_index
            aqi["main_pollution"] = main_pollution
            aqi["aqi_level"] = aqi_level
            aqi["time"] = update_time

            pollution_table = city_aqi_div.select("table tbody")[1]
            pollution_table_tr = pollution_table.find_all("tr")

            pollutions = []
            for tr in pollution_table_tr:
                tds = tr.find_all("td")
                poll = {
                    "pollution": tds[0].string,
                    "index": tds[1].string
                }
                pollutions.append(poll)

            aqi["pollutions"] = pollutions
            self.write(json.dumps(aqi))

        except HTTPError:
            self.write("HTTPError caught")

