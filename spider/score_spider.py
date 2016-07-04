import time
import requests
import mysql.connector
from bs4 import BeautifulSoup


def crawl_detail_info(url):
    chrome = requests.get(url)
    www = BeautifulSoup(chrome.text, "html5lib")
    div = www.find(id="pointbyarea")
    trs = div.find_all("tr")
    scores = []
    for n in range(1, len(trs)):
        tds = trs[n].find_all("td")
        score = {
            "year": str(tds[0].string),
            "min_score": str(tds[1].string),
            "max_score": str(tds[2].string),
            "avg_score": str(tds[3].string),
            "enrollment_num": str(tds[4].string),
            "enrollment_batch": str(tds[5].string),
        }
        scores.append(score)
    return scores

if __name__ == "__main__":
    crawl_detail_info("http://college.gaokao.com/school/tinfo/97/result/16/1/")

    config = {
        'user': 'root',
        'password': 'p4sswOrd',
        'host': '10.150.50.203',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    insert_sql = ("INSERT INTO score_sc"
                  "(school, subject, year, min_score, max_score, avg_score, enrollment_num, enrollment_batch)"
                  " VALUES (%(school)s, %(subject)s, %(year)s, %(min_score)s, %(max_score)s, %(avg_score)s,"
                  "%(enrollment_num)s, %(enrollment_batch)s)"
                  )

    template_url = "http://college.gaokao.com/schpoint/a16/b16/p{0}/"
    total_page = 60
    for n in range(1, 61):
        print("Precessing page {0}".format(n))
        page_url = template_url.format(n)
        browser = requests.get(page_url)
        html = BeautifulSoup(browser.text, "html5lib")
        score_list_div = html.find("div", class_="scores_List")
        dls = score_list_div.find_all("dl")

        for dl in dls:
            school = dl.find("strong", class_="blue").find("a").string
            subject = dl.find_all("li")[2].string
            subject = subject.split('：')[1]
            print("PAGE{0}: {1}---{2}".format(n, school, subject))
            link = dl.find("span", class_="blue").find("a")["href"]

            for item in crawl_detail_info(link):
                item["school"] = str(school)
                item["subject"] = str(subject)
                cursor.execute(insert_sql, item)
            time.sleep(3)
        conn.commit()
        time.sleep(3)

    cursor.close()
    conn.close()

