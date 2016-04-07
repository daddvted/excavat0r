# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mysql.connector

from engine.Linguist import Linguist

category = "A"

config = {
    'user': 'root',
    'password': 'hello',
    'host': '192.168.110.222',
    'port': '3306',
    'database': 'ai1',
    'raise_on_warnings': True,
}

linguist = Linguist(True, True)

conn = mysql.connector.connect(**config)
cursor_query = conn.cursor(buffered=True)
cursor_update = conn.cursor(buffered=True)

query_sql = "SELECT id, question FROM %s" % category

cursor_query.execute(query_sql)

for qid, question in cursor_query:
    cat, attrs = linguist.get_category(question)
    bits = linguist.get_bits(cat, attrs)
    bits_int = int(bits, 2)
    update_sql = "UPDATE %s SET bits_int=%s WHERE id=%s" % (category, bits_int, qid)
    cursor_update.execute(update_sql)

conn.commit()
cursor_query.close()
cursor_update.close()
conn.close()
