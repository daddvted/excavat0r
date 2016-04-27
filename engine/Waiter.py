# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import mysql.connector
import os.path
import xapian

from .Element import Element


class Waiter(Element):

    config = {
        'user': 'root',
        'password': 'hello',
        # 'host': '192.168.1.68',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'excavator',
        'raise_on_warnings': True,
    }

    def __init__(self):
        super(Waiter, self).__init__()

    @staticmethod
    def get_time(lang="cn"):
        if lang == "cn":
            now = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        else:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return now

    def _search_index(self, category, keywords_left):
        db_name = "dat/index/" + category
        db_path = os.path.join(self.base_path, db_name)
        index_db = xapian.WritableDatabase(db_path, xapian.DB_OPEN)
        enquire = xapian.Enquire(index_db)
        query_parser = xapian.QueryParser()
        query_parser.set_database(index_db)

        query_list = []

        print "[ Waiter.py - _search_index() ]", "keywords used for search: ", "|".join(keywords_left)

        for word in keywords_left:
            query = query_parser.parse_query(
                word,
                xapian.QueryParser.FLAG_AUTO_SYNONYMS
            )
            query_list.append(query)

        # final_query = xapian.Query(xapian.Query.OP_OR, query_list)
        final_query = xapian.Query(xapian.Query.OP_AND, query_list)
        enquire.set_query(final_query)

        matches = enquire.get_mset(0, 30, None)
        print "[ Waiter.py - _search_index() ]", "%s matches found" % matches.get_matches_estimated()

        qid_list = []
        for m in matches:
            qid_list.append(m.docid)

        return qid_list

    def get_answer(self, category, keywords_left):
        answer_list = []
        qid_list = self._search_index(category, keywords_left)

        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()

        if len(qid_list):
            for qid in qid_list:
                query = "SELECT question FROM %s WHERE id=%i" % (category, qid)
                cursor.execute(query)
                for result in cursor:
                    answer_list.append({
                        "qid": qid_list[0],
                        "title": result[0]
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
