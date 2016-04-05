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

    def _set_attr_bit(self, attr_list):
        cat = ""
        categories = {
            'A': ["社保", "社保局", "养老保险", "医疗保险", "生育保险", "工伤保险", "失业保险"],
            'B': ["出入境", "通行证", "护照", "签注", "签证"],
            'C': ["公积金", "住房公积金"],
        }

        hit = 0
        for attr in attr_list:
            for k in categories.keys():
                if attr in categories[k]:
                    cat = k
                    hit = 1
                    attr_list.remove(attr)
                    break
            if hit:
                break
        print cat
        print "after extract category: ", "|".join(attr_list)
        matrix = [
            ["办理", "办", "申请", "申办", "申领"],  # 0
            ["局", "管理局", "管理中心", "中心", "机构", "办事处"],  # 1
            ["地址", "地点", "地方", "哪里", "那里"],  # 2
            ["港澳", "台湾", '港澳台'],  # 3
            ["户口", "户籍"],  # 4
            ["异省", "外地", "异地", "外省"],  # 5
            ["请问", "咨询"],  # 6
            ["缴费", "缴存"],  # 7
            ["时间", "多久"],  # 8
            ["过期"],  # 9
            ["进度"],  # 10
        ]
        bits = []
        for attr in attr_list:
            s = ""
            for synonym in matrix:
                if attr in synonym:
                    s = '1' + s
                else:
                    s = '0' + s
            bits.append(s)
        final_bit = 0
        for bit in bits:
            final_bit |= int(bit, 2)

        bits_id = bin(final_bit)[2:]
        print bits_id
        return cat + bits_id
        # return str(final_bit)

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

    def analyze_semantic(self, sentence):
        # words = extract_tags(sentence, 5, allowPOS=('n', 'ns'))
        # words = extract_tags(sentence, topK=10, withWeight=True)

        # Extract top 5 keywords(tag)
        # "words" is a list, the 1st element is always the category
        # keyword which is set with the highest priority in "idf.txt"
        words = extract_tags(sentence, topK=5)
        print "keywords:", "|".join(words)  # debug

        code = self._set_attr_bit(words)
        print code
        return code
