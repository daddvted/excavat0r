# -*- coding: utf-8 -*-

# Chinese unicode range [u'\u4e00', u'\u9fa5']
# English unicode range [u'\u0041', u'\u005a'] and [u'\u0061', u'\u007a']
# Number unicode range [u'\u0030', u'\u0039']

cn = "你好"
en = "Hello"
mix = "傻B"

# uni = '\u4f60\u597d'
# print uni.decode('unicode_escape')
# ld = "吹牛逼"
# print type(ld)
# ld = ld.decode('utf-8')
# print type(ld)

ucn = cn.decode('utf-8')
# ucn = en.decode('utf-8')
# ucn = mix.decode('utf-8')

chn_flag = 0
eng_flag = 0
num_flag = 0
otr_flag = 0

total_length = len(ucn)

for i in ucn:
    if u'\u4e00' <= i <= u'\u9fa5':
        chn_flag += 1
    elif u'\u0041' <= i <= u'\u005a' and u'\u0061' <= i <= u'\u007a':
        eng_flag += 1
    elif u'\u0030' <= i <= u'\u0039':
        num_flag += 1
    else:
        otr_flag += 1

print chn_flag
print eng_flag
print num_flag
print otr_flag



