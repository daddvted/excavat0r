# -*- coding: utf-8 -*-
from jieba import posseg

# Chinese unicode range [u'\u4e00', u'\u9fa5']
# English unicode range [u'\u0041', u'\u005a'] and [u'\u0061', u'\u007a']
# Number unicode range [u'\u0030', u'\u0039']

cn = "你好"
en = "Hello"
mix = "傻B"
sen = "会议的日期"

# uni = '\u4f60\u597d'
# print uni.decode('unicode_escape')
# ld = "吹牛逼"
# print type(ld)
# ld = ld.decode('utf-8')
# print type(ld)


