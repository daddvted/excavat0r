import re
import requests
import lxml.html
from bson.objectid import ObjectId
from pymongo import MongoClient
from spider.Utils import fake_useragent


class UniversitySpider(object):
    PROVINCE = {
        "1": "北京",
        "2": "天津",
        "3": "上海",
        "4": "重庆",
        "5": "河北",
        "6": "河南",
        "7": "山东",
        "8": "山西",
        "9": "安徽",
        "10": "江西",
        "11": "江苏",
        "12": "浙江",
        "13": "湖北",
        "14": "湖南",
        "15": "广东",
        "16": "广西",
        "17": "云南",
        "18": "贵州",
        "19": "四川",
        "20": "陕西",
        "21": "青海",
        "22": "宁夏",
        "23": "黑龙江",
        "24": "吉林",
        "25": "辽宁",
        "26": "西藏",
        "27": "新疆",
        "28": "内蒙古",
        "29": "海南",
        "30": "福建",
        "31": "甘肃",
        "32": "港澳台",
    }

    def __init__(self):
        self.tracker = open("univ.txt", 'w')
        self.url_template = "http://kaoshi.edu.sina.com.cn/college/collegelist/view?provid=&typeid=&pro=&tab=&page={}"
        pass

    def crawl(self, start, end):
        for p in range(start, end + 1):
            headers = {
                "User-Agent": fake_useragent()
            }
            browser = requests.get(self.url_template.format(p), headers=headers)
            browser.encoding = "utf-8"
            if browser.status_code == 200:
                html = lxml.html.fromstring(browser.text)
                lis = html.xpath('//ul[@class="tabsContainer_ul"]/li')

                # Universities of current page
                for li in lis:
                    # University url like:
                    # http://kaoshi.edu.sina.com.cn/college/c/10001.shtml
                    url = li.xpath('./a')[0].attrib["href"]

                    # Extract university id from url
                    match = re.findall(r'/(\d+)\.shtml', url)
                    uid = int(match[0]) if match else 0

                    divs = li.xpath('.//div[@class="clearfix"]')

                    # Extract name, weibo
                    links = divs[0].xpath('.//a')
                    name = links[0].text_content().strip()
                    num = len(links)
                    weibo_official = "-"
                    weibo_enrollment_office = "-"
                    for n in range(1, num):
                        text = links[n].text_content().strip()
                        if text == "官方微博":
                            weibo_official = links[n].attrib["href"]

                        if text == "招办微博":
                            weibo_enrollment_office = links[n].attrib["href"]

                    # Extract info
                    ps = divs[1].xpath('.//p')
                    location = ps[0].text_content().strip().split(':')[1].strip()
                    utype = ps[2].text_content().strip().split(':')[1].strip()
                    subject_to = ps[4].text_content().strip().split(':')[1].strip()
                    key_discipline = re.findall(r'(\d+)', ps[1].text_content().strip())[0]
                    master = re.findall(r'(\d+)', ps[3].text_content().strip())[0]
                    doctor = re.findall(r'(\d+)', ps[5].text_content().strip())[0]

                    # Extract tags
                    tags = []
                    spans = divs[2].xpath('.//span')
                    for span in spans:
                        tags.append(span.text_content().strip())

                    doc = {
                        "uid": uid,  # 学校ID
                        "name": name,  # 学校名称
                        "weibo_official": weibo_official,  # 官方微博
                        "weibo_enrollment_office": weibo_enrollment_office,  # 招办微博
                        "location": location,  # 所在地
                        "utype": utype,  # 类别
                        "subject_to": subject_to,  # 隶属
                        "key_discipline": key_discipline,  # 重点学科
                        "master": master,  # 硕士点数
                        "doctor": doctor,  # 博士点数
                        "tags": tags,  # 标签
                        "url": url,  # 第二次抓取用url
                    }
                    print(doc)

                print("Page{:>6}: [done]".format(p))
                print("Page{:>6}: [done]".format(p), file=self.tracker)
            else:
                print("Page{:>6}: [fail]".format(p))
                print("Page{:>6}: [fail]".format(p), file=self.tracker)


class UniversityScoreSpider(object):
    pass


if __name__ == "__main__":
    univ = UniversitySpider()
    univ.crawl(1, 2)
    # conn = MongoClient("192.168.86.86:27017")
    # conn.service.authenticate('serviceadmin', 'hello', mechanism='SCRAM-SHA-1')
    # db = conn["service"]
    # university = db.university
    # university.update_one({"name": "北京大学"}, {"$set": {"name": "北京小学"}})
    # for doc in university.find({}):
    #     print(doc)
