# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tornado.web
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


class DebugHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("debug.html")


class EnquireHandler(tornado.web.RequestHandler):
    router = MessageRouter()

    def get(self):
        self._process_http_method()

    def post(self):
        self._process_http_method()

    def _process_http_method(self):
        try:
            message = json_decode(self.request.body)
            # Debug
            if "code" in message:
                result = self.router.debug_routing(message)
            else:
                result = self.router.routing(message)  # result is also a dict
            self.write(json_encode(result))

        except MissingArgumentError:
            self.return_except_err("MissingArgumentError")

        except ValueError:
            self.return_except_err("ArgumentValueError")

    def return_except_err(self, err):
        result = {
            "type": "999",
            "resp": err
        }
        self.write(json_encode(result))


class FeedbackHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    
    def post(self):
        pass
    
    def _process_http_method(self):
        pass
