# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mysql.connector

config = {
    'user': 'root',
    'password': 'hello',
    'host': '192.168.86.86',
    'port': '3306',
    'database': 'ai1',
    'raise_on_warnings': True,
}

cat = "B"
conn = mysql.connector.connect(**config)
cursor = conn.cursor()
query = "SELECT answer, bits_int FROM qa WHERE category='%s'" % cat
cursor.execute(query)

for (answer, bits_int) in cursor:
    print answer, bits_int


cursor.close()
conn.close()



