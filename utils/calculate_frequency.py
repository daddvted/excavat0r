# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import mysql.connector
import jieba.posseg as seg

from engine.Linguist import Linguist

config = {
    'user': 'root',
    'password': 'hello',
    'host': '192.168.110.222',
    'port': '3306',
    'database': 'ai1',
    'raise_on_warnings': True,
}

linguist = Linguist(True)
conn = mysql.connector.connect(**config)
cursor = conn.cursor()
# query = "SELECT question FROM cd_fund"
# query = "SELECT question_title, question_desc FROM cd_exit_entry"
query = "SELECT question FROM cd_social_security"
cursor.execute(query)
frequency = {}
for result in cursor:
    for r in result:  # result contains selected columns
        r = r.strip()
        words = seg.cut(r)
        for w, p in words:
            new_key = "%s|%s" % (w, p)
            if new_key in frequency:
                frequency[new_key] += 1
            else:
                frequency[new_key] = 1

# clean none chn key
for k in frequency.keys():
    # if 'chn' not in Linguist.lang_differ(k):
    new_key = k.split('|')[0]
    if 'chn' not in linguist.differentiate_lang(k):
        del(frequency[k])


# Write to file
sorted_list = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
# fh = codecs.open("cd_fund_freq.txt", 'w', encoding='utf-8')
# fh = codecs.open("cd_exit_entry_freq.txt", 'w', encoding='utf-8')
fh = codecs.open("cd_social_security_freq.txt", 'w', encoding='utf-8')
for s in sorted_list:
    line = "%s %s\n" % (s[0], s[1])
    fh.write(line)
fh.close()

cursor.close()
conn.close()
