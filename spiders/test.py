# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import codecs
import re
import urllib
import requests
from bs4 import BeautifulSoup

data = {
    "id": "1102f614-b51b-f8de-9e2a-11ec58af6b67"
}
r = requests.post("http://www.cdwh.org//wh/guide/getGuidById", data=data)
d = json.loads(r.text)

dd = d["data"][0]
content = dd["contents1"]


html = urllib.unquote(content)
print html
# new_html = re.sub(r'%u', r'\u', html)
# print new_html


