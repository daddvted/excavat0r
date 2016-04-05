# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import codecs
import jieba
import jieba.posseg as pseg
from jieba.analyse import extract_tags


class Linguist:
    categories = {}
    matrix = []

    def __init__(self):
        jieba.load_userdict("dat/dict.txt")

        with codecs.open("dat/categories.json", "r", "utf-8") as c:
            self.categories = json.load(c)
        with codecs.open("dat/matrix.json", "r", "utf-8") as m:
            self.matrix = json.load(m)

    def _differentiate_char(self, uchar):
        flag = 4  # 0-cn, 1-en, 2-num, 3-other
        if u'\u4e00' <= uchar <= u'\u9fa5':
            flag = 0
        elif u'\u0041' <= uchar <= u'\u005a' or u'\u0061' <= uchar <= u'\u007a':
            flag = 1
        elif u'\u0030' <= uchar <= u'\u0039':
            flag = 2
        return flag

    def _set_attr_bit(self, attr_list):
        bits = []
        for attr in attr_list:
            s = ""
            for synonym in self.matrix:
                if attr in synonym:
                    s = '1' + s
                else:
                    s = '0' + s
            bits.append(s)
        final_bit = 0
        for bit in bits:
            final_bit |= int(bit, 2)

        bits_id = bin(final_bit)[2:]  # bin(xxx) output '0b11011'
        return bits_id

    def categorizer(self, sentence):
        key_num = len(self.matrix)
        tags = extract_tags(sentence, topK=key_num)
        print "Before: ", "|".join(tags)
        cat = ""
        hit = 0
        for t in tags:
            for k in self.categories.keys():
                if t in self.categories[k]:
                    cat = k
                    hit = 1
                    tags.remove(t)
                    break
            if hit:
                break

        if not hit:
            return 'X', '0'
        else:  # To the end of this function
            print "After: ", "|".join(tags)
            bits = self._set_attr_bit(tags)
            return cat, bits

    # ====================================
    # Test function
    # ====================================
    def extrac_keyword_code(self, sentence):
        # Extract top 5(length of the attributes matrix) keywords(tag)
        # "words" is a list, the 1st element is always the category
        # keyword which is set with the highest priority in "idf.txt"
        cat, bits = self.categorizer(sentence)

        return cat, bits

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
