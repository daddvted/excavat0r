# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tornado.web
from tornado.web import MissingArgumentError
from tornado.escape import json_decode
from tornado.escape import json_encode

from .MessageRouter import MessageRouter
from .Debugger import Debugger


class Default(tornado.web.RequestHandler):
    def get(self):
        self.write("oops 404")


class API(tornado.web.RequestHandler):
    router = MessageRouter()

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        # self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        try:
            message = {"msg": self.get_argument("msg")}
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


class Feedback(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        pass

    def _process_http_method(self):
        pass


class Debug(tornado.web.RequestHandler):
    debugger = Debugger()

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def get(self):
        message = {"code": self.get_argument("code"), "msg": self.get_argument("msg")}

        result = self.debugger.debug_routing(message)
        self.write(json_encode(result))
