# -*- encoding: utf-8 -*-
import tornado.web
import tornado.websocket
from tornado.websocket import WebSocketClosedError


from .Segment import *

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message("[Server] Ready")

    def on_message(self, message):
        tp = message[:3]

        # echo
        if tp == '000':
            msg =  message[3:]
            self.send_msg(msg)
        # segment
        elif tp == '001':
            msg = message[3:]
            tmp = "/ ".join(segment(msg))

            self.send_msg(tmp)

    def on_close(self):
        # self.write_message("[Server] Bye")
        self.close()

    def send_msg(self, message):
        try:
            self.write_message("[Server] " + message)

        except WebSocketClosedError:
            self.close()
