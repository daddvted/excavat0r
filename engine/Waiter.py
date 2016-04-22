# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import mysql.connector


class Waiter:
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.1.68',
        # 'host': '192.168.86.86',
        'port': '3306',
        'database': 'excavator',
        'raise_on_warnings': True,
    }

    @staticmethod
    def get_time(lang="cn"):
        if lang == "cn":
            now = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        else:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return now

    def get_answer(self, category, qid_list):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()

        answer_list = []
        print "[ Waiter.py - get_answer() ]", "question id", qid_list

        # if len(qid_list) == 1:
        #     query = "SELECT answer FROM %s WHERE id=%i" % (category, qid_list[0])
        #     cursor.execute(query)
        #     for result in cursor:
        #         answer_list.append({
        #             "qid": qid_list[0],
        #             "content": result[0]
        #         })
        # else:
        for qid in qid_list:
            query = "SELECT question FROM %s WHERE id=%i" % (category, qid)
            cursor.execute(query)
            for result in cursor:
                answer_list.append({
                    "qid": qid_list[0],
                    "content": result[0]
                })

        cursor.close()
        conn.close()
        return answer_list

    def commit_question(self, question):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        insert_stmt = (
            "INSERT INTO question2answer(question) VALUES(%s)"
            # "INSERT INTO question2answer(question, question2) VALUES(%s,%s)"
        )
        data = (question,)
        cursor.execute(insert_stmt, data)
        conn.commit()

        cursor.close()
        conn.close()
