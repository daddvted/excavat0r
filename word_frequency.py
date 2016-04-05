# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import codecs
import jieba
import mysql.connector

from engine.Linguist import Linguist

config = {
    'user': 'root',
    'password': 'hello',
    'host': '10.150.50.201',
    'port': '3306',
    'database': 'ai1',
    'raise_on_warnings': True,
}

linguist = Linguist()
conn = mysql.connector.connect(**config)
cursor = conn.cursor()
# query = "SELECT question_title from exit_and_entry LIMIT 3"
query = "SELECT question_title, question_desc FROM exit_and_entry"
cursor.execute(query)
frequency = {}
for title in cursor:
    # process "question_title"
    question = re.sub(ur'\[普通\]', '', title[0])
    question = question.strip()
    words = jieba.cut(question)
    for w in words:
        if frequency.has_key(w):
            frequency[w] += 1
        else:
            frequency[w] = 1

    # process "question_desc"
    question = title[1]
    question = question.strip()
    for w in words:
        if frequency.has_key(w):
            frequency[w] += 1
        else:
            frequency[w] = 1


# clean none chn key
for k in frequency.keys():
    if 'chn' not in linguist.lang_differ(k):
        del(frequency[k])

# Write to file
sorted_list = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
fh = codecs.open("frequency.txt", 'w', encoding='utf-8')
for s in sorted_list:
    line = "%s %s\n" %(s[0],s[1])
    fh.write(line)
fh.close()

cursor.close()
conn.close()
