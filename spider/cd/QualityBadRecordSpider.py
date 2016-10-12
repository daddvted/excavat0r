"""
产品质量监督抽查不良记录查询
URL: http://www.zjj.chengdu.gov.cn/cdzj/xxcx/cpzlbljlcxfw/list/
爬取日期: 2016-7-20
"""
import json
import requests
import lxml.html
import mysql.connector
from urllib.parse import urlencode
from spider.Utils import fake_useragent


class QualityBadRecordSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,
    }
    url = "http://www.zjj.chengdu.gov.cn/webi/qz/execute.do"

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def save2db(self, data):

        template = ("INSERT INTO quality_bad_record(name, enterprise, time) "
                    "VALUES (%(name)s, %(enterprise)s, %(time)s)")
        self.cursor.execute(template, data)
        self.conn.commit()

    def crawl(self):
        print("====== Processing page 1 ======")

        headers = {
            "User-Agent": fake_useragent(),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "name": "xxcx_cpzlbljlcxfw",
            "sql": "",
            "title": "产品质量监督抽查不良记录查询",
            "orderby": "",
            "startpage": "1",
            "pageSize": "500",
            "mode": "hdjl",
            "refresh": "true",
            "paging": "true",
            "align": "center",
            "queryed": "true",
            "searched": "true",
            "columnSetting": '[{"code":"cpflmc","show":false},{"code":"cpmc","display":"产品名称","show":true,"width":"250","reminder":""},{"code":"qymc","display":"企业名称","width":"200","reminder":""},{"code":"cjsj","display":"抽检时间","width":"70","reminder":""}]',
            "searchSetting": '[{"columnname":"cpmc","label":"产品名称","labelWidth":"100","columnSpan":"","inputWidth":"185","inputSpan":"","compare":"like","columnvalue":"","rownum":"1","colnum":"1"},{"columnname":"qymc","label":"企业名称","labelWidth":"100","columnSpan":"","inputWidth":"185","inputSpan":"","compare":"like","columnvalue":"","rownum":"1","colnum":"2"},{"columnname":"cjsj","label":"抽检时间","labelWidth":"100","columnSpan":"","inputWidth":"185","inputSpan":"","compare":"like","columnvalue":"","rownum":"1","colnum":"3"},{"columnname":"cpflmc","label":"产品分类","labelWidth":"100","columnSpan":"","inputWidth":"185","inputSpan":"","compare":"like","columnvalue":"","rownum":"1","colnum":"4"}]',
            "functionSetting": '[]'
        }
        browser = requests.post(self.url, headers=headers, data=urlencode(data), timeout=60)

        if browser.status_code == 200:
            result = json.loads(browser.text)
            html = lxml.html.fromstring(result["data"])
            trs = html.xpath('//div[@class="mem_tbls"]/table/tr')
            print(len(trs))
            for n in range(1, len(trs)):
                print("------ processing no {} ------".format(n))
                tds = trs[n].xpath('.//td')
                data = {
                    "name": tds[0].text_content().strip(),
                    "enterprise": tds[1].text_content().strip(),
                    "time": tds[2].text_content().strip(),
                }
                self.save2db(data)
        else:
            print("Error when crawling page")


if __name__ == "__main__":
    spider = QualityBadRecordSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()
