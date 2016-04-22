# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .Guesser import Guesser
from .TextMan import TextMan
from .Robot import Robot
from .SpiderMan import SpiderMan
from .Waiter import Waiter


class MessageRouter:
    def __init__(self):
        self.robot = Robot()
        self.waiter = Waiter()
        self.spiderman = SpiderMan()
        self.textman = TextMan()
        self.guesser = Guesser()
        self.categories = ["A", "B", "C"]

    # Receive dict and return dict
    def routing(self, message):
        help_text = """
        对不起, 在我的知识库里没有找到相关的回答<br/>
        需要将您的问答提交给客服人员回答么? <a id="400" href="#">提交</a>
        """
        code = message["code"]
        msg = message["msg"]

        response_code = ""
        response = None

        # ====================================
        #              Fake AI
        # ====================================
        if code == '000':
            category, category_key, keywords_left = self.textman.parse_category(msg)
            # if cat != "X":
            if category in self.categories:
                question_ids = self.textman.seek(category, keywords_left)
                if len(question_ids):
                    response_code = "000"
                    response = self.waiter.get_answer(category, question_ids)
                else:
                    response_code = "001"
                    response = help_text
            else:
                response_code = "999"
                response = self.robot.jabber()

        elif code == '400':
            self.waiter.commit_question(msg)
            response_code = "401"
            response = "提交成功, 请耐心等待"

        # ====================================
        #               Debug
        # ====================================
        # segment
        elif code == '901':
            response_code = "901"
            response = TextMan.segment(msg)
        # segment for search
        elif code == '904':
            response_code = "904"
            response = TextMan.segment_for_search(msg)

        # keywords extraction
        elif code == '902':
            response_code = "902"
            keyword_str = " | ".join(self.textman.extract_keyword(msg))
            response = keyword_str
        # extract SPO
        elif code == '905':
            response_code = "905"
            response = self.guesser.extract_spo(msg)
        # word flag
        elif code == '903':
            flags = TextMan.tag(msg)
            resp_list = []
            for word, flag in flags:
                resp_list.append({
                    "word": word,
                    "flag": flag,
                })

            response_code = "903"
            response = resp_list

        print "[ MessageRouter.py - routing()]", response_code, response
        return {"code": response_code, "resp": response}
