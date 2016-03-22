import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from engine.Handler import *

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
        ]

        settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                # data_path=os.path.join(os.path.dirname(__file__), "data"),
                xsrf_cookies=True,
                cookie_secret="__WITH_GREATE_POWER_COMES_WITH_GREATE_RESPONSIBILITY__",
                debug=True,
        )

        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
