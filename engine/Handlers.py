# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import tornado.web
import tornado.websocket
from tornado.websocket import WebSocketClosedError

from .MessageRouter import MessageRouter


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class WSHandler(tornado.websocket.WebSocketHandler):
    router = MessageRouter()

    def _send2client(self, message):
        try:
            self.write_message(message)
        except WebSocketClosedError:
            self.close()

    def check_origin(self, origin):
        return True

    def open(self):
        self._send2client("Ready")

    def on_message(self, message):
        code = message[:3]
        msg = message[3:]
        if code == '009':
            self._send2client("Wait a second")
        result = self.router.routing(code, msg)
        cat = result[0]
        bits = result[1:]
        bits_int = int(bits, 2)

        self._send2client(cat + str(bits_int))

    def on_close(self):
        self.close()
