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
        help_text = """
        对不起, 在我的知识库里没有找到相关的回答<br/>
        需要将您的问答提交给客服人员回答么? <a id="400" href="#">提交</a>
        """
        code = message["code"]
        msg = message["msg"]
        # ====================================
        #              Fake AI
        # ====================================
        if code == '000':
            cat, cat_key, key_list = self.linguist.filter_category(msg)
            # if cat != "X":
            if cat in self.category:
                question_ids = self.linguist.seek(cat, key_list)
                if len(question_ids):
                    resp = self.waiter.get_answer(cat, question_ids)
                    return {"type": "000", "resp": resp}
                else:
                    return {"type": "001", "resp": help_text}
            else:
                return {"type": "999", "resp": self.robot.jabber()}

        elif code == '400':
            self.waiter.commit_question(msg)
            return {"type": "401", "resp": "提交成功, 请耐心等待"}


        # ====================================
        #               Debug
        # ====================================
        # segment
        elif code == '901':
            result = {"type": code, "resp": Linguist.segment(msg)}
            # return json.dumps(result)  # JSON formatted str
            return result
        # segment for search
        elif code == '904':
            result = {"type": code, "resp": Linguist.segment_for_search(msg)}
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
