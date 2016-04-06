# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mysql.connector

from .Linguist import Linguist
from .Robot import Robot
from .SpiderMan import SpiderMan
from .Waiter import Waiter


class MessageRouter:

    def __init__(self):
        self.robot = Robot()
        self.waiter = Waiter()
        self.spiderman = SpiderMan()
        self.linguist = Linguist(True, True)

        # init db connection

    def routing(self, code, msg):
        # ====================================
        #              Fake AI
        # ====================================
        if code == '000':
            config = {
                'user': 'root',
                'password': 'hello',
                'host': '192.168.110.222',
                'port': '3306',
                'database': 'ai1',
                'raise_on_warnings': True,
            }

            html = "<div>"

            cat, attrs = self.linguist.get_category(msg)
            print cat
            if cat == "A":
                bits = self.linguist.get_bits(cat, attrs)
                return "公积金%s" % bits
            elif cat == "B":
                bits = self.linguist.get_bits(cat, attrs)
                return "出入境%s" % bits
            elif cat == "C":
                bits = self.linguist.get_bits(cat, attrs)
                return "社保%s" % bits
            else:
                return "I don't understand :/"
                # attr_int = int(bits, 2)
                # conn = mysql.connector.connect(**config)
                # cursor = conn.cursor()
                # query = "SELECT answer, bits_int FROM qa WHERE category='%s'" % cat
                # cursor.execute(query)
                # for (answer, bits_int) in cursor:
                #     if attr_int == (attr_int & bits_int):
                #         html += "<p>%s</p>" % answer
                #
                # html += "</div>"
                # cursor.close()
                # conn.close()
                # return html

        # ====================================
        #               Debug
        # ====================================
        # segment
        elif code == '001':
            return "| ".join(Linguist.segment(msg))

        # keywords extraction
        elif code == '002':
            return "|".join(Linguist.extract_keyword_code(msg))

        # word flag
        elif code == '003':
            flags = Linguist.tag(msg)
            html = "<ul>"
            for word, flag in flags:
                html += "<li>" + word + ":" + flag + "</li>"
            html += "</ul>"
            return html
        elif code == '004':
            cat, bits = self.linguist.extract_keyword_code(msg)
            if cat == 'X':
                return "I don't understand :/"
            else:
                bits_int = int(bits, 2)

                return "%s | %d | %s" % (cat, bits_int, bits)

