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


class HTTPHandler(tornado.web.RequestHandler):
    router = MessageRouter()

    def get(self):
        self.http_handler()

    def post(self):
        self.http_handler()

    def http_handler(self):
        try:
            message = json_decode(self.request.body)
            print type(message)
            result = self.router.routing(message)  # result is also a dict
            self.write(json_encode(result))

        except MissingArgumentError:
            self.return_except_err("MissingArgumentError")

        except ValueError:
            self.return_except_err("ArgumentValueError")

    def return_except_err(self, str):
        result = {
            "type": "999",
            "resp": str
        }
        self.write(json_encode(result))


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
