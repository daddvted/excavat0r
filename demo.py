from tornado.httpclient import HTTPClient, HTTPRequest
from urllib.parse import urlencode

# url = "http://www.zaichengdu.com/api/nightwork"
url = "http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_querySmXz.do"
# url = "http://www.zaichengdu.com/api/aq"

data = {
    "code": "033",
    "ajbjg": "5002240300",
    "bfwjgmc": "",
    "afwjglx": "医院",
    "ayydj": "",
}

header = {
    "Content-Type": "application/x-www-form-urlencoded",
}

req = HTTPRequest(url, method="POST", headers=header, body=urlencode(data))
resp = HTTPClient().fetch(req)

print(resp.code)
print(resp.body.decode('utf-8'))
