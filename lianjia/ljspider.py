import os
import requests


class HouseSpider(object):
    total_page = 100
    dir_name = "secondhand"

    def __init__(self):
        # self.url_tpl = "http://cd.fang.lianjia.com/loupan/pg{}/"
        self.url_tpl = "http://cd.lianjia.com/ershoufang/pg{}/"
        try:
            os.mkdir(self.dir_name)
        except FileExistsError:
            pass

    def crawl(self):
        for p in range(1, self.total_page + 1):
            browser = requests.get(self.url_tpl.format(p))
            browser.encoding = "utf-8"

            with open("{}/{}.html".format(self.dir_name, p), 'w') as f:
                f.write(browser.text)

            print("Page{:>6}: [done]".format(p))

if __name__ == "__main__":
    house_new = HouseSpider()
    house_new.crawl()
