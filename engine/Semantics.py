# -*- encoding: utf-8 -*-
import jieba


def segment(sentence):
    segment_result = jieba.cut(sentence, cut_all=True)
    # segment_result = jieba.cut(sentence, cut_all=False)
    return segment_result


def lang_differ(sentence):
    sentence.decode('utf-8')
    chn_flag = 0
    eng_flag = 0
    num_flag = 0
    otr_flag = 0
