# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jieba
import jieba.posseg
import nltk

sentence1 = "大王叫我来巡山"
sentence2 = "小明想买一个非常绿的帽子"
sentence3 = "我今天非常想查询我的成都市的公积金"
# sentence3 = "我今天非常想查询我的成都市的住房公积金"

pairs = jieba.posseg.cut(sentence3)

pos = []
for w, p in pairs:
    pos.append((w, p))

grammar = r"""
    SUB:
        {^<n|nr|r>+.*}
    PRE:
        {.*<v|vd|vg|vn>+.*}
    OBJ:
        {.*<n|nr>+$}
    """
# grammar = "TGT: {.*<uj><n|np>}"

rp = nltk.RegexpParser(grammar)
result = rp.parse(pos)


extraction = {}
for r in result:
    if isinstance(r, nltk.tree.Tree):
        for leaf in r.leaves():
            phrase = ""
            phrase += leaf[0]
        extraction[r.label()] = phrase

print extraction
result.draw()
