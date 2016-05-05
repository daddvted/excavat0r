# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import codecs


service = {}

with codecs.open("../dat/service.json", "r", "utf-8") as srv:
    service = json.load(srv)


print service

