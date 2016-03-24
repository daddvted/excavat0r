# -*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

import re
import codecs
import requests
from bs4 import BeautifulSoup

# url = 'http://zhidao.baidu.com/search?word=%B3%C9%B6%BC'
url = 'http://wenda.so.com/search/?q=成都'

headers = {
    # "host": "zhidao.baidu.com",
    "host": "wenda.so.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "Accept-Encoding",
}

page = requests.get(url, headers=headers)
page.encoding = 'utf-8'
print page.status_code
html = re.sub(ur'href="(/q/.+)"', ur'href="http://www.abc.com\1"', page.text)
soup = BeautifulSoup(html, "html5lib")
# html = soup.find(id="wgt-list")
# html = soup.select(".qa-list")[0]
html = soup.find("ul", class_="qa-list")
print unicode(html)

