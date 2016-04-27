# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from .Robot import Robot
from .Waiter import Waiter
from .TextMan import TextMan
from .SpiderMan import SpiderMan
from .SemanticMan import SemanticMan


class MessageRouter:
    def __init__(self):
        self.robot = Robot()
        self.waiter = Waiter()
        self.textman = TextMan()
        self.spiderman = SpiderMan()
        self.semanticman = SemanticMan()
        self.categories = ["A", "B", "C"]

        self.response_code = ""
        self.response = None

        self.help_text = """
        不好意思, 您的问题我暂时回答不了<br/>
        我已经将您的问题<b>提交</b>给客服人员回答<br/>
        谢谢使用!
        """

    @staticmethod
    def _categorize(category):
        if category == "A":
            category_tuple = ["公积金", "公积金管理中心"]
        elif category == "B":
            category_tuple = ["出入境", "出入境管理局"]
        elif category == "C":
            category_tuple = ["社保", "社保局"]

        return category_tuple

    # Receive dict and return dict
    def routing(self, message):
        msg = message["msg"]

        # Step 1: categorizing sentence
        category, category_key, keywords_left = self.textman.parse_category(msg)

        # Step 2A: Category in categories list(["A","B","C"])
        if category in self.categories:

            # Step 3A: Keywords left after parse_category()
            if len(keywords_left):
                # Answer returned without analyze user's sentence,
                # only using keyword extraction
                answer_list = self.waiter.get_answer(category, keywords_left)

                # Step 4A: Find answer according to user's sentence
                if len(answer_list):
                    self.response_code = "000"
                    self.response = answer_list
                    return self._send_response()
                # Step 4B: Find no answer, ready to perform _parse_sentence_step()
                else:
                    # Step 5A: At this point, Check whether user is asking a place
                    if re.search(ur'哪里|那里', msg):
                        self.response_code = "002"
                        kw = self._categorize(category)
                        print "kw ", kw
                        self.response = {"kw": kw[1]}
                        return self._send_response()

                    # Step 5B: Finally using _parse_sentence_step()
                    else:
                        self._do_sentence_parsing(category, msg)
                        return self._send_response()

            # Step 3B: No keyword left after parse_category().
            # Maybe the user input single keyword like "社保" or "公积金".
            else:
                self._do_single_keyword(category, msg)
                return self._send_response()

        # Step 2B: category is 'X', means the sentence is nonsense
        else:
            self.response_code = "999"
            self.response = self.robot.jabber()
            return self._send_response()

    def _do_sentence_parsing(self, category, sentence):
        print "parsing sentence structure"
        sentence_structure = self.semanticman.analyze_structure(sentence)

        new_sentence = ""
        if "PRE" in sentence_structure:
            new_sentence += "".join(sentence_structure['PRE'])
        if "OBJ" in sentence_structure:
            new_sentence += "".join(sentence_structure['OBJ'])
        print "[ MessageRouter.py - _parse_sentence_step(): new_sentence ]", new_sentence

        new_keywords = self.textman.extract_keyword(new_sentence)
        answer_list = self.waiter.get_answer(category, new_keywords)
        if len(answer_list):
            self.response_code = "000"
            self.response = answer_list
        else:
            self.response_code = "400"
            self.response = self.help_text
            self.waiter.commit_question(sentence)

    def _do_single_keyword(self, category, sentence):
        print "_single_keyword_step", category

        param = self._categorize(category)
        guess_text = """
        您在询问<span style="color: red;">%s</span>, 是想办理<b>%s</b>相关业务吗, 我为您找到<b>%s</b>的地图信息
        """ % (sentence, param[0], param[1])
        self.response_code = "001"
        self.response = {"text": guess_text, "kw": param[1]}

    def _send_response(self):
        # print "[ MessageRouter.py - _send_response()]", response_code, response
        return {"code": self.response_code, "resp": self.response}

