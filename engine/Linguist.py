# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import codecs
import os.path

import jieba.analyse
import jieba.posseg as pseg
import xapian


class Linguist:
    categories = {}

    def __init__(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.path.dirname(file_path)

        jieba.load_userdict(os.path.join(self.base_path, "dat/self_idf.txt"))
        # jieba.load_userdict(self_dict)

        with codecs.open(os.path.join(self.base_path, "dat/categories.json"), "r", "utf-8") as c:
            self.categories = json.load(c)

    @staticmethod
    def _differentiate_char(uchar):
        flag = 4  # 0-cn, 1-en, 2-num, 3-other
        if u'\u4e00' <= uchar <= u'\u9fa5':
            flag = 0
        elif u'\u0041' <= uchar <= u'\u005a' or u'\u0061' <= uchar <= u'\u007a':
            flag = 1
        elif u'\u0030' <= uchar <= u'\u0039':
            flag = 2
        return flag

    def differentiate_lang(self, sentence):
        # u_sentence = sentence.decode('utf-8')
        # total_length = len(u_sentence)
        chn_flag = 0
        eng_flag = 0
        num_flag = 0
        otr_flag = 0

        for word in sentence:
            flag = self._differentiate_char(word)
            # flag = Linguist._differentiate_char(word)
            if flag == 0:
                chn_flag += 1
            elif flag == 1:
                eng_flag += 1
            elif flag == 2:
                num_flag += 1
            else:
                otr_flag += 1

        lang = []
        if chn_flag > 0:
            lang.append('chn')
        if eng_flag > 0:
            lang.append('eng')
        if num_flag > 0:
            lang.append('num')
        if otr_flag > 0:
            lang.append('otr')
        return lang

    def extract_keyword(self, sentence):
        jieba.analyse.set_idf_path(os.path.join(self.base_path, "dat/self_idf.txt"))
        return jieba.analyse.extract_tags(sentence)

    # def get_bits(self, cat=None, attr_list=None):
    #     if len(attr_list):
    #         with codecs.open(os.path.join(self.base_path, "dat/matrix.json"), "r", "utf-8") as m:
    #             tmp = json.load(m)
    #
    #         matrix = tmp[cat]
    #         bits = []
    #         for attr in attr_list:
    #             s = ""
    #             for synonym in matrix:
    #                 if attr in synonym:
    #                     s = '1' + s
    #                 else:
    #                     s = '0' + s
    #             bits.append(s)
    #         final_bit = 0
    #         for bit in bits:
    #             final_bit |= int(bit, 2)
    #
    #         bits_id = bin(final_bit)[2:]  # bin(xxx) output '0b11011'
    #         return bits_id
    #     else:
    #         return '0'

    # def get_category(self, sentence):
    #     jieba.analyse.set_idf_path(os.path.join(self.base_path, "dat/self_idf.txt"))
    #     tags = jieba.analyse.extract_tags(sentence, topK=32)
    #     cat = ""
    #     hit = 0
    #     for t in tags:
    #         for k in self.categories.keys():
    #             if t in self.categories[k]:
    #                 cat = k
    #                 hit = 1
    #                 tags.remove(t)
    #                 break
    #         if hit:
    #             break
    #
    #     if not hit:
    #         return 'X', []
    #     else:  # To the end of this function
    #         return cat, tags
    def get_category(self, sentence):
        tags = self.extract_keyword(sentence)
        print "[ Linguist.py - get_category() ]", tags
        cat = ""
        hit = 0
        for t in tags:
            for k in self.categories.keys():
                if t in self.categories[k]:
                    cat = k
                    hit = 1
                    break
            if hit:
                break
        if not hit:
            return 'X'
        else:
            return cat

    def seek(self, category, sentence):
        print "[ Linguist.py - seek() ]", "Category: %s" % category
        db_name = "dat/index/" + category
        db_path = os.path.join(self.base_path, db_name)
        index_db = xapian.WritableDatabase(db_path, xapian.DB_OPEN)
        enquire = xapian.Enquire(index_db)
        query_parser = xapian.QueryParser()
        query_parser.set_database(index_db)

        query_list = []
        print "[ Linguist.py - seek() ]", "Sentence keywords: ", "|".join(self.extract_keyword(sentence))
        for word in self.extract_keyword(sentence):
            query = query_parser.parse_query(
                word,
                xapian.QueryParser.FLAG_AUTO_SYNONYMS
            )
            query_list.append(query)

        final_query = xapian.Query(xapian.Query.OP_AND, query_list)
        enquire.set_query(final_query)

        matches = enquire.get_mset(0, 30, None)
        print "[ Linguist.py - seek() ]", "%s matches found" % matches.get_matches_estimated()

        qid_list = []
        for m in matches:
            print m
            qid_list.append(m.docid)

        return qid_list

    # ====================================
    #           Test function
    # ====================================

    # Return segmented list
    @staticmethod
    def segment(sentence):
        return " | ".join(jieba.cut(sentence, cut_all=False))

    @staticmethod
    def tag(sentence):
        return pseg.cut(sentence)
