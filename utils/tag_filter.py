# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs

# filename = "cd_fund_freq.txt"
filename = "exit_entry_freq.txt"

tag = {}
filter_list = ["j", "n", "ns", "nt", "nz", "v", "vn", "x"]

file_in = codecs.open(filename, 'r', 'utf-8')
file_out = codecs.open("filtered_"+filename, 'w', 'utf-8')

for line in file_in:
    line = line.strip()
    kw, _ = line.split()
    w, p = kw.split('|')
    if p in filter_list:
        file_out.write("%s\n" % line)

file_in.close()
file_out.close()


