# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .Linguist import Linguist
from .Robot import Robot
from .SpiderMan import SpiderMan
from .Waiter import Waiter


class MessageRouter:
    def __init__(self):
        self.robot = Robot()
        self.waiter = Waiter()
        self.spiderman = SpiderMan()
        self.linguist = Linguist()

        # init db connection

    def routing(self, code, msg):
        # ====================================
        #              Fake AI
        # ====================================
        if code == '000':
            cat = self.linguist.get_category(msg)
            if cat != "X":
                question_ids = self.linguist.seek(cat, "".join(msg))
                return self.waiter.get_answer_html(cat, question_ids)

            else:
                return "I don't understand :/"

        # ====================================
        #               Debug
        # ====================================
        # segment
        elif code == '901':
            return "|".join(Linguist.segment(msg))

        # keywords extraction
        elif code == '902':
            return "|".join(self.linguist.extract_keyword(msg))
            # return "|".join(Linguist.extract_keyword(msg))

        # word flag
        elif code == '903':
            flags = Linguist.tag(msg)
            html = "<ul>"
            for word, flag in flags:
                html += "<li>" + word + ":" + flag + "</li>"
            html += "</ul>"
            return html

