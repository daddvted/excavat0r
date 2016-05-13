# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import codecs
import os.path


class Element(object):
    def __init__(self):
        self_path = os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.path.dirname(self_path)
        self.dict_file = "dat/dict.txt"
        self.chat_file = "dat/chat.txt"
        self.service_dict = {}

    def init_service(self):
        service_file = "dat/service.json"
        with codecs.open(os.path.join(self.base_path, service_file), 'r', 'utf-8') as srv:
            try:
                self.service_dict = json.load(srv)
            except ValueError as err:
                print "FORMAT ERROR [ service.json ]: %s" % err
                exit()
