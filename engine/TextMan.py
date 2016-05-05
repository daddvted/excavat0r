# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path
import jieba.analyse
import jieba.posseg

from .Element import Element


class TextMan(Element):
    service = {}

    def __init__(self):
        super(TextMan, self).__init__()

        self.init_service()

        jieba.load_userdict(os.path.join(self.base_path, self.dict_file))
        self.tf_idf = jieba.analyse.TFIDF(os.path.join(self.base_path, self.dict_file))

    @staticmethod
    def differentiate_char(uchar):
        flag = 3  # 0-cn, 1-en, 2-num, 3-other
        if u'\u4e00' <= uchar <= u'\u9fa5':
            flag = 0
        elif u'\u0041' <= uchar <= u'\u005a' or u'\u0061' <= uchar <= u'\u007a':
            flag = 1
        elif u'\u0030' <= uchar <= u'\u0039':
            flag = 2
        return flag

    def differentiate_lang(self, sentence):
        chn_flag = 0
        eng_flag = 0
        num_flag = 0
        otr_flag = 0

        for word in sentence:
            flag = self.differentiate_char(word)
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

    def extract_keyword(self, sentence, num=10, weight=False):
        return self.tf_idf.extract_tags(sentence, topK=num, withWeight=weight)

    def parse_category(self, sentence):
        keywords_left = self.extract_keyword(sentence)
        print "[ TextMan.py - parse_category() ]", "Original keyword: ", "|".join(keywords_left)
        category = ""
        category_keyword = ""
        hit = 0
        for t in keywords_left:
            print t, "@@"
            for k in self.service.keys():
                print self.service[k]["kw"]
                if t in self.service[k]["kw"]:
                    category = k
                    category_keyword = t
                    keywords_left.remove(t)
                    hit = 1
                    break
            if hit:
                break
        if not hit:
            return 'X', "", []
        else:
            return category, category_keyword, keywords_left

    # ====================================
    #           Debug function
    # ====================================

    # Return segmented list
    @staticmethod
    def segment(sentence):
        return " | ".join(jieba.cut(sentence, cut_all=False))

    @staticmethod
    def segment_for_search(sentence):
        return " | ".join(jieba.cut_for_search(sentence))

    @staticmethod
    def tag(sentence):
        return jieba.posseg.cut(sentence)
