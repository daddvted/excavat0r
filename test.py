# -*- coding: utf-8 -*-

import json
import codecs
import jieba.posseg as pseg
from jieba.analyse import extract_tags
from jieba.analyse import TextRank

d = {}
with codecs.open('dat/service.json','r','utf-8') as f:
    d = json.load(f)

k0 = d.keys()

# question = "咨询护照办理"
question = "外地人口，在郫县上学怎么办理护照？"

words = pseg.cut(question)
for w, p in words:
    print "%s - %s" %(w, p)
print "---------------------"
tags = extract_tags(question, allowPOS=['n','ns'])

for tag in tags:
    if tag in k0:
        print "here"
        print tag
        print d[k0]
