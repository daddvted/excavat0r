# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path


class Element(object):

    def __init__(self):
        self_path = os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.path.dirname(self_path)
        self.dict_file = "dat/dict.txt"
        self.category_file = "dat/categories.json"
        self.chat_file = "dat/chat.txt"
