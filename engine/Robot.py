# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import os.path
from .Element import Element


class Robot(Element):
    chat = []

    def __init__(self):
        super(Robot, self).__init__()
        with open(os.path.join(self.base_path, self.chat_file), 'r') as chat_data:
            self.chat = chat_data.readlines()

    def jabber(self):
        return random.choice(self.chat)
