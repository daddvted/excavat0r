# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .SemanticMan import SemanticMan
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
        self.semanticman = SemanticMan()
        self.categories = ["A", "B", "C"]

        self.response_code = ""
        self.response = None

        self.help_text = """
        对不起, 您的问题我暂时回答不了<br/>
        需要将您的问题提交给客服人员回答么? <a id="400" href="#">提交</a>
        """

    # Receive dict and return dict
    def routing(self, message):
        msg = message["msg"]

        # 1st, parse category of the sentence
        category, category_key, keywords_left = self.textman.parse_category(msg)

        # Category in categories list(["A","B","C"])
        if category in self.categories:

            if len(keywords_left):
                # Answer returned without analyze user's sentence,
                # only using keyword extraction
                answer_list = self.waiter.get_answer(category, keywords_left)
                if len(answer_list):
                    self.response_code = "000"
                    self.response = answer_list
                    return self._send_response()
                else:
                    self._parse_sentence_step(category, msg)
                    return self._send_response()
            # No keywords_left
            # user input single keyword like "社保"
            else:
                self._single_keyword_step()

        # Category is 'X', means the sentence is nonsense
        else:
            self.response_code = "999"
            self.response = self.robot.jabber()
            return self._send_response()

        # Question can not be answered by ai, commit to CS
        # elif code == '400':
        #     self.waiter.commit_question(msg)
        #     self.response_code = "401"
        #     self.response = "提交成功, 请耐心等待"
        #     return self._send_response()

    def _parse_sentence_step(self, category, sentence):
        print "parsing sentence structure"
        sentence_structure = self.semanticman.analyze_structure(sentence)
        new_sentence = ""
        new_sentence += "".join(sentence_structure['PRE'])
        new_sentence += "".join(sentence_structure['OBJ'])
        print "new_sentence in step_2a_analysis", new_sentence
        new_keywords = self.textman.extract_keyword(new_sentence)
        answer_list = self.waiter.get_answer(category, new_keywords)
        if len(answer_list):
            self.response_code = "000"
            self.response = answer_list
        else:
            self.response_code = "400"
            self.response = self.help_text

    def _single_keyword_step(self):
        print "Single keyword !!!"

    def _send_response(self):
        # print "[ MessageRouter.py - _send_response()]", response_code, response
        return {"code": self.response_code, "resp": self.response}

    # ====================================
    #                DEBUG
    # ====================================
    # Receive dict and return dict
    def debug_routing(self, message):
        code = message["code"]
        msg = message["msg"]

        # segment
        if code == '901':
            self.response_code = "901"
            self.response = TextMan.segment(msg)
            return self._send_debug_response()
        # segment for search
        elif code == '904':
            self.response_code = "904"
            self.response = TextMan.segment_for_search(msg)
            return self._send_debug_response()
        # keywords extraction
        elif code == '902':
            self.response_code = "902"
            self.response = " | ".join(self.textman.extract_keyword(msg))
            return self._send_debug_response()
        # extract sentence structure
        elif code == '905':
            self.response_code = "905"
            self.response = self.semanticman.analyze_structure(msg)
            return self._send_debug_response()
        # word flag
        elif code == '903':
            flags = TextMan.tag(msg)
            resp_list = []
            for word, flag in flags:
                resp_list.append({
                    "word": word,
                    "flag": flag,
                })
            self.response_code = "903"
            self.response = resp_list
            return self._send_debug_response()
            # ====================================
            #               Debug(end)
            # ====================================

    def _send_debug_response(self):
        # print "[ MessageRouter.py - _send_response()]", response_code, response
        return {"code": self.response_code, "resp": self.response}
