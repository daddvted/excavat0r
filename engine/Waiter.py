# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import mysql.connector


class Waiter:
    def __init__(self):
        config = {
            'user': 'root',
            'password': 'hello',
            'host': '192.168.1.26',
            # 'host': '192.168.110.222',
            'port': '3306',
            'database': 'ai1',
            'raise_on_warnings': True,
        }
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    @staticmethod
    def get_time(lang="cn"):
        if lang == "cn":
            now = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        else:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return now

    def get_answer(self, category, qid_list):
        answer_list = []

        if len(qid_list) == 1:
            query = "SELECT answer FROM %s WHERE id=%i" % (category, qid_list[0])
            self.cursor.execute(query)
            for result in self.cursor:
                answer_list.append(result[0])
        else:
            for qid in qid_list:
                query = "SELECT question FROM %s WHERE id=%i" % (category, qid)
                self.cursor.execute(query)
                for result in self.cursor:
                    html += '<li><a href="#">%s</a></li>' % result[0]
                html += "</ul></div>"

        return answer_list
