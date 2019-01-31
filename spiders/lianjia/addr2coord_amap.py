import json
import requests


def addr2coord(addr):
    api = "http://restapi.amap.com/v3/geocode/geo?address={}&output=JSON&key={}&city={}"
    key = "2ca63b5c854c29fc700e0cc9afd6492d"
    city = "成都市"
    url = api.format(addr, key, city)

    browser = requests.get(url)
    result = json.loads(browser.text)

    try:
        coords = result["geocodes"]
        if len(coords):
            coord = coords[0]["location"].split(",")
            return dict(zip(["lng", "lat"], coord))
        else:
            return {}
    except KeyError:
        print("here")
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

    with open("house_points_amap.json", "w") as f:
        json.dump(data, f)
