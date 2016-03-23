# -*- encoding: utf-8 -*-
import time
import tornado.web
import tornado.websocket
from tornado.websocket import WebSocketClosedError

from .Semantics import *
from .Robot import Robot


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message("[Server] Ready")

    def on_message(self, message):
        code = message[:3]

        # AI
        if code == '000':
            # message = message[3:]
            robot = Robot()
            self._send2client(robot.jabber())
        # segment
        elif code == '001':
            message = message[3:]
            tmp = "/ ".join(segment(message))
            self._send2client(tmp)
        # language identify
        elif code == '002':
            message = message[3:]
            tmp = lang_differ(message)
            self._send2client(tmp)
        # echo
        elif code == '009':
            self._send2client("Wait a seconds")
            time.sleep(1)
            message = message[3:]
            self._send2client(message)

    def on_close(self):
        self.close()

    def _send2client(self, message):
        try:
            self.write_message("[Server] " + message)

        except WebSocketClosedError:
            self.close()
