# -*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
from bs4 import BeautifulSoup

url = 'http://zhidao.baidu.com/search?word=%B3%C9%B6%BC'

headers = {
    "host": "zhidao.baidu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "Accept-Encoding",
}

resp = requests.get(url, headers=headers)

soup = BeautifulSoup(resp.text, "html5lib")
html = soup.find(id="wgt-list")
title = html.find_all('a', class_="ti")
for ti in title:
    print ti.em.string

# for item in soup.select("ol li"):
#    num = item.find("em").string
#    rate = item.select(".rating_num")[0].string
#    title = item.find("span").string
