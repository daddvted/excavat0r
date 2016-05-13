# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import mysql.connector
import jieba.posseg

from engine.TextMan import TextMan
from engine.TextMan import differentiate_lang


service_list = ["SS"]
filter_list = ["j", "n", "nz", "ns", "v", "vn", "x"]
word_length = 2

config = {
    'user': 'root',
    'password': 'hello',
    'host': '192.168.1.91',
    'port': '3306',
    'database': 'excavator',
    'raise_on_warnings': True,
}

textman = TextMan()
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

for service in service_list:
    query = "SELECT question FROM %s" % service
    cursor.execute(query)
    frequency = {}
    for result in cursor:
        for txt in result:  # result contains selected columns
            txt = txt.strip()
            words = jieba.posseg.cut(txt)
            for w, p in words:
                # filter
                if len(w) >= word_length and p in filter_list:
                    new_key = (w, p)

                if new_key in frequency:
                    frequency[new_key] += 1
                else:
                    frequency[new_key] = 1

    # remove none chn key
    for k in frequency.keys():
        new_key = k[0]
        if 'chn' not in differentiate_lang(new_key):
            del(frequency[k])

    # Write to file
    sorted_list = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    fh = codecs.open("frequency_%s.txt" % service, 'w', encoding='utf-8')
    for s in sorted_list:
        line = "%s|%s|%d\n" % (s[0][0], s[0][1], s[1])
        fh.write(line)

    fh.close()

cursor.close()
conn.close()
