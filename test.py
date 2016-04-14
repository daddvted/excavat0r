# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

d = {
    "type": "903",
    "msg": [
        ("a", "A"),
        ("b", "B"),
        ("c", "C"),
    ]
}

print json.dumps(d)

