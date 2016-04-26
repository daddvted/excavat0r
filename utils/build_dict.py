# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os.path
import codecs


category_list = ["A", "C"]
categories = {}

file_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(file_path)

idf = codecs.open(os.path.join(base_path, "dat/dict.txt"), "w", "utf-8")

with codecs.open(os.path.join(base_path, "dat/categories.json"), "r", "utf-8") as c:
    categories = json.load(c)

# Write category line first with weight 100
for l in categories.values():
    for item in l:
        line = "%s 200\n" % item
        idf.write(line)

# Then write filtered frequent word with weight 90
for category in category_list:
    filename = "frequency_%s.txt" % category
    with codecs.open(filename, "r", "utf-8") as freq:
        for line in freq:
            line = line.strip()
            words = line.split('|')
            new_line = "%s %d\n" % (words[0], 100+int(words[2]))
            idf.write(new_line)

idf.close()
