# -*- encoding: utf-8 -*-
import jieba


def segment(sentence):
    segment_result = jieba.cut(sentence, cut_all=True)
    # segment_result = jieba.cut(sentence, cut_all=False)
    return segment_result


def lang_differ(sentence):
    pass
