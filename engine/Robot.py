# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
from .Element import Element


class Robot(Element):
    chat = []

    def __init__(self):
        super(Robot, self).__init__()
        with open(self.base_path + "/dat/chat.txt", 'r') as chat_dat:
            self.chat = chat_dat.readlines()

    def jabber(self):
        return random.choice(self.chat)
