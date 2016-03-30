# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import codecs
import jieba
import jieba.posseg as pseg
from jieba.analyse import extract_tags


class Linguist:
    tags = {}

    def __init__(self):
        jieba.load_userdict("dat/dict.txt")
        with codecs.open("dat/tags.json", "r", "utf-8") as t:
            self.tags = json.load(t)

    def _differentiate_char(self, uchar):
        flag = 4  # 0-cn, 1-en, 2-num, 3-other
        if u'\u4e00' <= uchar <= u'\u9fa5':
            flag = 0
        elif u'\u0041' <= uchar <= u'\u005a' or u'\u0061' <= uchar <= u'\u007a':
            flag = 1
        elif u'\u0030' <= uchar <= u'\u0039':
            flag = 2
        return flag

    def segment(self, sentence):
        # segment_result = jieba.cut(sentence, cut_all=True)
        segment_result = jieba.cut(sentence, cut_all=False)
        return segment_result

    def tag(self, sentence):
        words = pseg.cut(sentence)
        return words

    def lang_differ(self, sentence):
        # u_sentence = sentence.decode('utf-8')
        # total_length = len(u_sentence)
        chn_flag = 0
        eng_flag = 0
        num_flag = 0
        otr_flag = 0

        for word in sentence:
            flag = self._differentiate_char(word)
            if flag == 0:
                chn_flag += 1
            elif flag == 1:
                eng_flag += 1
            elif flag == 2:
                num_flag += 1
            else:
                otr_flag += 1

        lang = "|"
        if chn_flag > 0:
            lang += "中文|"
        if eng_flag > 0:
            lang += "英文|"
        if num_flag > 0:
            lang += "数字|"
        if otr_flag > 0:
            lang += "其它|"

        return lang

    def analyze_semantic(self, sentence):
        # words = extract_tags(sentence, 5, allowPOS=('n', 'ns'))
        # words = extract_tags(sentence, topK=10, withWeight=True)
        words = extract_tags(sentence, topK=5)
        # for w, wt in words:
        #     print w, wt
        return "|".join(words)
