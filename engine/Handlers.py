# -*- coding: utf-8 -*-
import tornado.web
import tornado.websocket
from tornado.websocket import WebSocketClosedError

from .AI import MessageHub


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class WSHandler(tornado.websocket.WebSocketHandler):
    hub = MessageHub()

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
        result = self.hub.msg_hub(code, msg)
        self._send2client(result)

    def on_close(self):
        self.close()
