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
                'host': '192.168.1.192',
                # 'host': '192.168.110.222',
                'port': '3306',
                'database': 'ai1',
                'raise_on_warnings': True,
            }
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            # cursor = conn.cursor(buffered=True)

            cat, attrs = self.linguist.get_category(msg)
            if cat != "X":
                html = "<div>"
                bits = self.linguist.get_bits(cat, attrs)
                bits_int_id = int(bits, 2)
                query_sql = "SELECT question, answer, bits_int FROM %s WHERE bits_int>=%d" % (cat, bits_int_id)
                cursor.execute(query_sql)
                print cursor.rowcount
                for question, answer, bits_int in cursor:
                    if bits_int & bits_int_id == bits_int_id:
                        html += '<p><a href="#">%s</a></p>' % question

                html += "</div>"

                return html
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
            return "|".join(self.linguist.extract_keyword(msg))
            # return "|".join(Linguist.extract_keyword(msg))

        # word flag
        elif code == '003':
            flags = Linguist.tag(msg)
            html = "<ul>"
            for word, flag in flags:
                html += "<li>" + word + ":" + flag + "</li>"
            html += "</ul>"
            return html
        elif code == '004':
            cat, attrs = self.linguist.get_category(msg)
            if cat == 'X':
                return "I don't understand :/"
            else:
                bits = self.linguist.get_bits(cat, attrs)
                bits_int = int(bits, 2)

                return "%s | %d | %s" % (cat, bits_int, bits)
