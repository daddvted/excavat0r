# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os.path
import codecs


service_list = ["FD", "SS", "EE"]
services = {}

file_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(file_path)

idf = codecs.open(os.path.join(base_path, "dat/dict.txt"), "w", "utf-8")

with codecs.open(os.path.join(base_path, "dat/service.json"), "r", "utf-8") as c:
    services = json.load(c)

# Write category line first with weight 200
for service in services.keys():
    for item in services[service]["kw"]:
        line = "%s 200\n" % item
        idf.write(line)

idf.close()
