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
        self.category = ["A", "B", "C"]

        # init db connection

    # Receive dict and return dict
    def routing(self, message):
        code = message["code"]
        msg = message["msg"]
        # ====================================
        #              Fake AI
        # ====================================
        if code == '000':
            cat = self.linguist.get_category(msg)
            # if cat != "X":
            if cat in self.category:
                question_ids = self.linguist.seek(cat, msg)
                resp = self.waiter.get_answer(cat, question_ids)
                return {"type": "000", "resp": resp}
            else:
                return {"type": "999", "resp": "What did you say ?"}

        # ====================================
        #               Debug
        # ====================================
        # segment
        elif code == '901':
            result = {"type": code, "resp": Linguist.segment(msg)}
            # return json.dumps(result)  # JSON formatted str
            return result

        # keywords extraction
        elif code == '902':
            keyword_str = " | ".join(self.linguist.extract_keyword(msg))
            result = {"type": code, "resp": keyword_str}
            return result

        # word flag
        elif code == '903':
            flags = Linguist.tag(msg)
            resp_list = []
            for word, flag in flags:
                resp_list.append({
                    "word": word,
                    "flag": flag,
                })

            result = {
                "type": code,
                "resp": resp_list
            }
            return result

