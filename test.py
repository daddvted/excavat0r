# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import codecs

from itertools import product

with codecs.open("dat/synonym.json", "r", "utf-8") as f:
    synonym = json.load(f)

print synonym

for k in synonym.keys():
    for syn_str in synonym[k]:
        for i in product(syn_str.split("|"), repeat=2):
            if not i[0] == i[1]:
                print



