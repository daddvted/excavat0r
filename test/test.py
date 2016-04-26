# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re


text1 = "你在哪里"
text2 = "你在那里"
text3 = "你在里"

if re.search(ur'哪里|那里', text3):
    print "found"
else:
    print "not found"

