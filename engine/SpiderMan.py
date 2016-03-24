# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


class SpiderMan:
    def fetch_answer(self, kw, site):
        # 0 - 360问答
        # 1 - 百度知道
        urls = [
            'http://wenda.so.com/search/?q=',
            'http://zhidao.baidu.com/search?word=',
        ]
        hosts = [
            'wenda.so.com',
            'zhidao.baidu.com',
        ]

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "Accept-Encoding",
        }
        url = urls[site]+kw
        headers["host"] = hosts[site]
        page = requests.get(url, headers=headers)
        page.encoding = 'utf-8'
        soup = BeautifulSoup(page.text, "html5lib")
        html = soup.find("ul", class_="qa-list")
        return unicode(html)
