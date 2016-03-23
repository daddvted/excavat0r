# -*- encoding: utf-8 -*-
import jieba
import random
import re


from datetime import datetime

input = "What time is it ?"
uinput = input.decode("utf-8")

keywords = [u"time", u"date", u"时间", u"日期"]
key = ("apple", "pear", "banana")

now_cn = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
now_en = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

str = "今天天气不错"
ustr = str.decode("utf-8")
re_ptn = re.compile(ur'天气')
m = re_ptn.search(ustr)
if m:
    print m.group(0)

