# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from engine.Handlers import *

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", Enquire),
            (r"/enquire", EnquireHandler),
            (r"/debug", Debug),
            (r"/debug_enquire", DebugHandler),
            (r"/feedback", FeedbackHandler),
        ]

        settings = dict(
                default_handler_class=Default,
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                data_path=os.path.join(os.path.dirname(__file__), "dat"),
                xsrf_cookies=False,
                # xsrf_cookies=True,
                cookie_secret="__WITH_GREAT_POWER_COMES_WITH_GREAT_RESPONSIBILITY__",
                debug=True,
                autoreload=True,
        )

        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
