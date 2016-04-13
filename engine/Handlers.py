# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import tornado.web
import tornado.websocket
from tornado.websocket import WebSocketClosedError
from tornado.escape import json_decode

from .MessageRouter import MessageRouter


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class MapHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("map.html")


class JsonHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json_decode('{hello:"world"}'))


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
        result = self.router.routing(code, msg)
        self._send2client(result)

    def on_close(self):
        self.close()
