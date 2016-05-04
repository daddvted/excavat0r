# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import codecs
import os.path
from itertools import product
import mysql.connector
import jieba
import xapian


class Indexing:
    def __init__(self, category):
        # Build base path
        self_path= os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.path.dirname(self_path)

        # Load synonyms
        with codecs.open(os.path.join(self.base_path, "dat/synonym.json"), "r", "utf-8") as syn:
            self.synonym = json.load(syn)

        # Init xapian DB
        index_db_path = "dat/index/" + category
        self.db = xapian.WritableDatabase(os.path.join(self.base_path, index_db_path), xapian.DB_CREATE_OR_OPEN)

    def index(self, qid, txt):
        doc = xapian.Document()
        for word in jieba.cut_for_search(txt):
            doc.add_term(word)
            key = ":%s" % qid
            doc.add_term(key)
            self.db.replace_document(key, doc)

    def fill_synonym(self, category):
        if category in self.synonym:
            for synonym_str in self.synonym[category]:
                for syn_tuple in product(synonym_str.split('|'), repeat=2):
                    if syn_tuple[0] != syn_tuple[1]:
                        print "%s, %s" % (syn_tuple[0], syn_tuple[1])
                        self.db.add_synonym(syn_tuple[0], syn_tuple[1])

        for synonym_str in self.synonym["ALL"]:
            print "ALL"
            for syn_tuple in product(synonym_str.split('|'), repeat=2):
                if syn_tuple[0] != syn_tuple[1]:
                    print "%s, %s" % (syn_tuple[0], syn_tuple[1])
                    self.db.add_synonym(syn_tuple[0], syn_tuple[1])

    def commit_db(self):
        self.db.commit()


if __name__ == "__main__":
    # ====================================
    # A - 住房公积金
    # B - 出入境
    # C - 社保
    # ====================================
    # category_list = ["A", "B", "C"]
    category_list = ["A", "C"]
    # category_list = ["C"]

    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.1.68',
        'port': '3306',
        'database': 'excavator',
        'raise_on_warnings': True,
    }
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    for cat in category_list:
        print "Indexing Category %s." % cat
        indexer = Indexing(cat)

        # changes this sql for different category
        query = "SELECT id, question FROM  %s" % cat
        cursor.execute(query)

        for q_id, title in cursor:
            indexer.index(q_id, title)

        indexer.fill_synonym(cat)
        indexer.commit_db()

    cursor.close()
    conn.close()
