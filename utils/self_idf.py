# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import codecs

categories = {}
matrix = []

with codecs.open("../dat/categories.json", "r", "utf-8") as c:
    categories = json.load(c)

with codecs.open("../dat/matrixA.json", "r", "utf-8") as m:
    matrix = json.load(m)

fh = codecs.open("self_idf.txt", "w", "utf-8")

for l in categories.values():
    for item in l:
        line = "%s 100\n" % item
        fh.write(line)

for l in matrix:
    for item in l:
        line = "%s 90.00\n" % item
        fh.write(line)

fh.close()
