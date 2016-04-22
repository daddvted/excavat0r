# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path
import jieba
import xapian
import nltk


class Guesser:
    def __init__(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.path.dirname(file_path)

    def seek(self, category, key_list):
        # keyword_used = 4
        print "[ TextMan.py - seek() ]", "Category: %s" % category
        db_name = "dat/index/" + category
        db_path = os.path.join(self.base_path, db_name)
        index_db = xapian.WritableDatabase(db_path, xapian.DB_OPEN)
        enquire = xapian.Enquire(index_db)
        query_parser = xapian.QueryParser()
        query_parser.set_database(index_db)

        query_list = []

        print "[ TextMan.py - seek() ]", "keywords used for search: ", "|".join(key_list)

        for word in key_list:
            query = query_parser.parse_query(
                word,
                xapian.QueryParser.FLAG_AUTO_SYNONYMS
            )
            query_list.append(query)

        # final_query = xapian.Query(xapian.Query.OP_OR, query_list)
        final_query = xapian.Query(xapian.Query.OP_AND, query_list)
        enquire.set_query(final_query)

        matches = enquire.get_mset(0, 30, None)
        print "[ TextMan.py - seek() ]", "%s matches found" % matches.get_matches_estimated()

        qid_list = []
        for m in matches:
            print m
            qid_list.append(m.docid)

        return qid_list

    def extract_spo(self, sentence):
        jieba.load_userdict(os.path.join(self.base_path, "dat/self_idf.txt"))
        pairs = jieba.posseg.cut(sentence)

        prepared_sentence = []
        for w, t in pairs:
            prepared_sentence.append((w, t))

        grammar = r"""
            SUB:
                {^<j|n|ng|nr|ns|nt|nz|r|x>+.*}
            PRE:
                {.*<v|vd|vg|vn>+.*}
            OBJ:
                {.*<j|n|nr|x>+$}
            ADV:
                {.*<p|r>+}
        """
        parser = nltk.RegexpParser(grammar)
        result = parser.parse(prepared_sentence)
        # result.draw()

        extraction = {}
        for r in result:
            if isinstance(r, nltk.tree.Tree):
                phrase = ""
                for leaf in r.leaves():
                    phrase += leaf[0]
                extraction[r.label()] = phrase
        return extraction
