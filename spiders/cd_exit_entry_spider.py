# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Spider for　成都市公安局出入境管理局－在线答疑
import time
import mysql.connector
import re
import randoms
import request
from bs4 import BeautifulSoup

user_agents = [
    "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MI NOTE LTE Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025489 Mobile Safari/533.1 MicroMessenger/6.3.13.49_r4080b63.740 NetType/cmnet Language/zh_CN",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MI NOTE LTE Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025489 Mobile Safari/533.1 MicroMessenger/6.3.13.49_r4080b63.740 NetType/cmnet Language/zh_CN",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 MicroMessenger/6.3.13 NetType/WIFI Language/zh_CN",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Shuame; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.1.1000 Chrome/39.0.2146.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)",
    "Googlebot/2.1 (http://www.googlebot.com/bot.html)",
    "Opera/9.20 (Windows NT 6.0; U; en)",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)",
]
host = "www.cdcrj.gov.cn"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
}

# Fetch total page
url = 'http://www.cdcrj.gov.cn/exitentry/zxkf.htm'
headers["User-Agent"] = random.choice(user_agents)
headers["host"] = host
page = requests.get(url, headers=headers)
page.encoding = 'utf-8'
soup = BeautifulSoup(page.text, "html5lib")
results = soup.find("div", class_="pagesite")
page_ptn = results.div.get_text()
m = re.search(r'[0-9]+/([0-9]+)', page_ptn)
total_page = int(m.group(1)) + 1

config = {
    'user': 'qa',
    'password': 'qa',
    'host': '192.168.110.222',
    'port': '3306',
    'database': 'qa',
    'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

for page_num in range(1, total_page):
    print "Processing page %s" % page_num
    time.sleep(3)
    url = "http://www.cdcrj.gov.cn/exitentry/zxkf_%s.htm" % (str(page_num))
    headers["User-Agent"] = random.choice(user_agents)
    headers["host"] = host
    page = requests.get(url, headers=headers)
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.text, "html5lib")
    results = soup.find_all("div", class_="lybMessage")

    for r in results:
        q_title = r.find("h1").string
        q_desc = r.find_all("span")[1].string
        answer = str(r.find("h4"))
        answer = re.sub(r'<h4>\s+', '<h4>', answer)
        answer = re.sub(r'\s+</h4>', '</h4>', answer)

        insert_stmt = (
            "INSERT INTO exit_and_entry(question_title, question_desc,answer) VALUES(%s, %s, %s)"
        )
        data = (q_title, q_desc, answer)
        cursor.execute(insert_stmt, data)
    cnx.commit()

cursor.close()
cnx.close()
