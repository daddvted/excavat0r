# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs

category_list = ["A", "C"]

tag = {}

filter_list = ["j", "n", "nz", "v", "vn", "x"]
word_length = 2

for category in category_list:
    filename = "frequency_%s.txt" % category
    file_in = codecs.open(filename, 'r', 'utf-8')
    file_out = codecs.open("filtered_"+filename, 'w', 'utf-8')

    for line in file_in:
        line = line.strip()
        kw, _ = line.split()
        w, p = kw.split('|')
        if len(w) >= word_length:
            if p in filter_list:
                file_out.write("%s\n" % line)

    file_in.close()
    file_out.close()


