# -*- coding: utf-8 -*-
import time
from .Linguist import Linguist
from .Waiter import Waiter
from .SpiderMan import SpiderMan
from .Robot import Robot


class MessageRouter:
    def __init__(self):
        self.robot = Robot()
        self.waiter = Waiter()
        self.spiderman = SpiderMan()
        self.linguist = Linguist()

    def routing(self, code, msg):
        kw = []
        # AI
        if code == '000':
            time_kw = [u"time", u"date", u"today", u"now", u"时间", u"日期", u"时刻"]
            for s in self.linguist.segment(msg):
                if s.lower() in time_kw:
                    return self.waiter.get_time()
            return self.spiderman.start2crawl(msg, 1)
            # return self.robot.jabber()
        # segment
        elif code == '001':
            return "/ ".join(self.linguist.segment(msg))
        # language identify
        elif code == '002':
            return self.linguist.lang_differ(msg)
        # word flag
        elif code == '003':
            flags = self.linguist.tag(msg)
            html = "<ul>"
            for word, flag in flags:
                html += "<li>" + word + ":" + flag + "</li>"
            html += "</ul>"
            return html

        # echo
        elif code == '009':
            time.sleep(1)
            return msg


