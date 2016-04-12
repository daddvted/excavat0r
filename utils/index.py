# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path
import mysql.connector
import jieba
import xapian


# class Index:
#     def __init__(self):
#         print "init"
#         self.file_path = os.path.dirname(os.path.abspath(__file__))
#         self.base_path = os.path.dirname(self.file_path)
#         jieba.load_userdict(os.path.join(self.base_path, "dat/self_idf.txt"))
#
#     @staticmethod
#     def index(db, id, txt):
#         doc = xapian.Document()
#         for word in jieba.cut_for_search(txt):
#             doc.add_term(word)
#             key = ":%s" % id
#             doc.add_term(key)
#             db.replace_document(key, doc)
#
#     @staticmethod
#     def commit_db(db):
#         db.commit()

def init_self_dict():
    file_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(file_path)
    jieba.load_userdict(os.path.join(base_path, "dat/self_idf.txt"))


def index(db, id, txt):
    doc = xapian.Document()
    for word in jieba.cut_for_search(txt):
        doc.add_term(word)
        key = ":%s" % id
        doc.add_term(key)
        db.replace_document(key, doc)


if __name__ == "__main__":
    init_self_dict()

    ####################################
    # A - 住房公积金
    # B - 出入境
    # C - 社保
    ####################################

    # category_list = ["A", "B", "C"]
    # category_list = ["A", "C"]
    category_list = ["C"]

    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.1.26',
        'port': '3306',
        'database': 'ai1',
        'raise_on_warnings': True,
    }

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    file_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(file_path)

    for category in category_list:
        print "Indexing Category %s." % category
        db_name = "dat/index/" + category
        db_path = os.path.join(base_path, db_name)
        index_db = xapian.WritableDatabase(db_path, xapian.DB_CREATE_OR_OPEN)

        # changes this sql for different category
        query = "SELECT id, question FROM  %s" % category
        cursor.execute(query)

        for qid, title in cursor:
            index(index_db, qid, title)
        if category == 'C':
            index_db.add_synonym("社会保险卡","社保卡")
            index_db.add_synonym("社保卡", "社会保险卡")
            index_db.commit()
        else:
            index_db.commit()

    cursor.close()
    conn.close()
