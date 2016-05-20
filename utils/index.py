# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import codecs
import os.path
from itertools import product
import mysql.connector
import jieba
import xapian

from engine.TextMan import TextMan
from engine.TextMan import filter_sentence


class Indexing:
    def __init__(self, service):
        # Build base path
        self_path= os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.path.dirname(self_path)
        self.tm = TextMan()

        # Load synonyms
        with codecs.open(os.path.join(self.base_path, "dat/synonym.json"), "r", "utf-8") as syn:
            self.synonym = json.load(syn)

        # Init xapian DB
        index_db_path = "dat/index/" + service
        self.db = xapian.WritableDatabase(os.path.join(self.base_path, index_db_path), xapian.DB_CREATE_OR_OPEN)

    def index(self, qid, txt):
        txt = filter_sentence(txt)

        # key = str(qid)
        key = "%s" % qid
        doc = xapian.Document()
        for word in jieba.cut_for_search(txt):
            doc.add_term(word)
            doc.add_term(key)

        self.db.replace_document(key, doc)

    def fill_synonym(self, service):
        if service in self.synonym:
            for synonym_str in self.synonym[service]:
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
    # FD - 住房公积金
    # EE - 出入境
    # SS - 社保
    # ====================================
    # service_list = ["FD", "EE", "SS"]
    service_list = ["FD", "SS"]

    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.1.91',
        'port': '3306',
        'database': 'excavator',
        'raise_on_warnings': True,
    }
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    for srv in service_list:
        print "Indexing Category %s." % srv
        indexer = Indexing(srv)

        # changes this sql for different category
        query = "SELECT id, question FROM  %s" % srv
        cursor.execute(query)

        for q_id, title in cursor:
            indexer.index(q_id, title)

        indexer.fill_synonym(srv)
        indexer.commit_db()

    cursor.close()
    conn.close()
