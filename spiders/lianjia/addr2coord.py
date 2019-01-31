import json
import requests


def addr2coord(addr):
    api = "http://api.map.baidu.com/geocoder/v2/?output=json&ak={}&city={}&address={}"
    key = "Wpi6NmGmbAxrQDl6NAOVdufUMPMHyofA"
    city = "成都市"
    url = api.format(key, city, addr)

    browser = requests.get(url)
    result = json.loads(browser.text)

    try:
        coord = result["result"]["location"]
        return coord
    except KeyError:
        return {}


if __name__ == "__main__":

    with open("newhouse/newhouse.json", "r") as f:
        houses = json.loads(f.read())

    data = []
    for house in houses:
        tmp = addr2coord(house["addr"])
        if tmp:
            price = int(house["avg_price"])
            price = price/100 if price > 100 else price
            tmp["count"] = int(price)
            print(tmp)
            data.append(tmp)
        else:
            continue

    with open("house_points.json", "w") as f:
        json.dump(data, f)