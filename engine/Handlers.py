# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import tornado.web
import tornado.websocket
from tornado.websocket import WebSocketClosedError
from tornado.escape import json_decode
from tornado.escape import json_encode

from .MessageRouter import MessageRouter


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


# class AI1Handler(tornado.web.RequestHandler):
#     router = MessageRouter()
#
#     def get(self):
#         msg = self.get_argument("m")
#         print msg
#         d = {
#             "hello": msg
#         }
#         self.write(json_encode(d))


class WSHandler(tornado.websocket.WebSocketHandler):
    router = MessageRouter()

    def send2client(self, message):
        try:
            self.write_message(message)
        except WebSocketClosedError:
            self.close()

    def check_origin(self, origin):
        return True

    def open(self):
        pass
        # self.send2client("Ready")

    def on_message(self, message):
        message = json_decode(message)  # message is a dict
        print "In Handler.py ", message
        result = self.router.routing(message)  # result is also dict
        self.send2client(json_encode(result))

    def on_close(self):
        self.close()
