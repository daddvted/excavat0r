# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os.path
import codecs

categories = {}
matrix = []

print os.path.realpath(__file__)
file_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(file_path)

with codecs.open(os.path.join(base_path, "dat/categories.json"), "r", "utf-8") as c:
    categories = json.load(c)

with codecs.open("../dat/matrixA.json", "r", "utf-8") as m:
    matrix = json.load(m)

fh = codecs.open(os.path.join(base_path, "dat/self_idf.txt"), "w", "utf-8")

for l in categories.values():
    for item in l:
        line = "%s 100\n" % item
        fh.write(line)

for l in matrix:
    for item in l:
        line = "%s 90.00\n" % item
        fh.write(line)

fh.close()
