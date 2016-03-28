# -*- coding: utf-8 -*-
import random
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
        user_agents = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MI NOTE LTE Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025489 Mobile Safari/533.1 MicroMessenger/6.3.13.49_r4080b63.740 NetType/cmnet Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 MicroMessenger/6.3.13 NetType/WIFI Language/zh_CN",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Shuame; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.1.1000 Chrome/39.0.2146.0 Safari/537.36"
        ]

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "Accept-Encoding",
        }
        url = urls[site]+kw
        headers["host"] = hosts[site]
        headers["User-Agent"] = random.choice(user_agents)

        page = requests.get(url, headers=headers)
        page.encoding = 'utf-8'
        soup = BeautifulSoup(page.text, "html5lib")
        html = soup.find("ul", class_="qa-list")
        return unicode(html)

