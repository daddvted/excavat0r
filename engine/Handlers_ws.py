# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tornado.web
import tornado.websocket
from tornado.websocket import WebSocketClosedError
from tornado.web import MissingArgumentError
from tornado.escape import json_decode
from tornado.escape import json_encode

from .MessageRouter import MessageRouter


class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("oops 404")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


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
        print "[ Handler.py - on_message() ]", message
        result = self.router.routing(message)  # result is also a dict
        self.send2client(json_encode(result))

    def on_close(self):
        self.close()
