import os
import glob
import json
import lxml.html


class NewHouseProcessor(object):
    DATA_PATH = "newhouse"
    BASE_URL = "http://cd.fang.lianjia.com"

    def process(self):

        houses = []

        os.chdir(self.DATA_PATH)
        for page in glob.glob("*.html"):
            with open(page, "r") as f:
                html = lxml.html.fromstring(f.read())
                divs = html.xpath('//div[@class="info-panel"]')
                for div in divs:
                    a = div.xpath('./div[@class="col-1"]/h2/a')[0]
                    name = a.text_content().strip()
                    url = self.BASE_URL + a.attrib["href"]

                    span = div.xpath('.//div[@class="where"]/span')[0]
                    addr = span.text_content().strip()

                    span = div.xpath('.//div[@class="average"]/span')

                    avg_price = 0
                    if len(span):
                        avg_price = span[0].text_content().strip()

                    house = {
                        "name": name,
                        "addr": addr,
                        "avg_price": avg_price,
                        "url": url
                    }

                    houses.append(house)

        print(len(houses))
        with open("newhouse.json", "w") as f:
            json.dump(houses, f)

if __name__ == "__main__":
    new_house = NewHouseProcessor()
    new_house.process()
