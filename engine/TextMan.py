# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path
import jieba.analyse
import jieba.posseg

from .Element import Element


def differentiate_char(uchar):
    # 0 - chn
    # 1 - eng
    # 2 - num
    # 3 - otr
    flag = 3
    if u'\u4e00' <= uchar <= u'\u9fa5':
        flag = 0
    elif u'\u0041' <= uchar <= u'\u005a' or u'\u0061' <= uchar <= u'\u007a':
        flag = 1
    elif u'\u0030' <= uchar <= u'\u0039':
        flag = 2
    return flag


def differentiate_lang(sentence):
    chn_flag = 0
    eng_flag = 0
    num_flag = 0
    otr_flag = 0

    for word in sentence:
        flag = differentiate_char(word)
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


def filter_sentence(sentence):
    new_sentence = []
    for char in sentence:
        if differentiate_char(char) == 0:
            new_sentence.append(char)

    return "".join(new_sentence)


class TextMan(Element):
    service = {}

    def __init__(self):
        super(TextMan, self).__init__()

        self.init_service()

        jieba.load_userdict(os.path.join(self.base_path, self.dict_file))
        self.tf_idf = jieba.analyse.TFIDF(os.path.join(self.base_path, self.dict_file))

    def extract_keyword(self, sentence, num=10, weight=False):
        # type: (object, object, object) -> object
        return self.tf_idf.extract_tags(sentence, topK=num, withWeight=weight)

    def parse_service_type(self, sentence):
        sentence = filter_sentence(sentence)
        keywords = self.extract_keyword(sentence)
        keywords_cut = list(jieba.cut(sentence))
        # keywords_cut = keywords
        print "[ TextMan.py - parse_category() ]", "Original keyword: ", "|".join(keywords)
        service_type = ""
        hit = 0
        for word in keywords:
            for k in self.service.keys():
                if word in self.service[k]["kw"]:
                    service_type = k
                    hit = 1
                    break
            if hit:
                break
        if not hit:
            return 'X', []
        else:
            return service_type, keywords_cut

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
