# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random


class Robot:
    chat = []

    def __init__(self):
        with open("dat/chat.txt", 'r') as chat_dat:
            self.chat = chat_dat.readlines()

    def jabber(self):
        return random.choice(self.chat)
