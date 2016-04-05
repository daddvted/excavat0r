# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import mysql.connector
from .Linguist import Linguist
from .Waiter import Waiter
from .SpiderMan import SpiderMan
from .Robot import Robot


class MessageRouter:
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.110.222',
        'port': '3306',
        'database': 'ai1',
        'raise_on_warnings': True,
    }

    def __init__(self):
        self.robot = Robot()
        self.waiter = Waiter()
        self.spiderman = SpiderMan()
        self.linguist = Linguist()

        # init db connection

    def routing(self, code, msg):
        kw = []
        # ====================================
        #            Fake AI
        # ====================================
        if code == '000':
            cat, bits = self.linguist.categorizer(msg)
            conn = mysql.connector.connect(**self.config)
            cursor = self.conn.cursor()
            query = ("SELECT answer, bits_int FROM qa "
                     "WHERE category='%s'")
            cursor.execute(self.query, cat)

            for (answer, bits_int) in cursor:
                print bits_int, answer

            cursor.close()
            conn.close()
            return "query db"

        # segment
        elif code == '001':
            return "/ ".join(self.linguist.segment(msg))

        # language identify
        elif code == '002':
            return "|".join(self.linguist.lang_differ(msg))

        # word flag
        elif code == '003':
            flags = self.linguist.tag(msg)
            html = "<ul>"
            for word, flag in flags:
                html += "<li>" + word + ":" + flag + "</li>"
            html += "</ul>"
            return html
        elif code == '004':
            cat, bits = self.linguist.extrac_keyword_code(msg)
            if cat == 'X':
                return "I don't understand :/"
            else:
                bits_int = int(bits, 2)

                return "%s | %d | %s" % (cat, bits_int, bits)

        # echo
        elif code == '009':
            time.sleep(1)
            return msg
