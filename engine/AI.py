# -*- coding: utf-8 -*-
import time
import random
from .Semantics import segment, lang_differ
from .Waiter import Waiter
from .SpiderMan import SpiderMan


class Robot:
    chat = []

    def __init__(self):
        with open("dat/chat.txt", 'r') as chat_dat:
            self.chat = chat_dat.readlines()

    def jabber(self):
        random.shuffle(self.chat)
        return self.chat[0]


class MessageHub:
    def __init__(self):
        self.robot = Robot()
        self.waiter = Waiter()
        self.spiderman = SpiderMan()

    def msg_hub(self, code, msg):
        kw = []
        # AI
        if code == '000':
            time_kw = [u"time", u"date", u"today", u"now", u"时间", u"日期", u"时刻"]
            for s in segment(msg):
                if s.lower() in time_kw:
                    return self.waiter.get_time()
            return self.spiderman.fetch_answer(msg, 0)
            # return self.robot.jabber()
        # segment
        elif code == '001':
            return "/ ".join(segment(msg))
        # language identify
        elif code == '002':
            return lang_differ(msg)
        # echo
        elif code == '009':
            time.sleep(1)
            return msg


