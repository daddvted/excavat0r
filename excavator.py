import os
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import define, options

from engine.Handlers import *
from engine.AirQuality import AirQualityHandler

define("port", default=8000, help="run on the given port", type=int)


class WWW(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", DebugHandler),
            (r"/aq", AirQualityHandler)
        ]

        settings = dict(
                default_handler_class=DefaultHandler,
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                data_path=os.path.join(os.path.dirname(__file__), "dat"),
                # xsrf_cookies=False,
                xsrf_cookies=True,
                cookie_secret="__WITH_GREAT_POWER_COMES_WITH_GREAT_RESPONSIBILITY__",
                debug=True,
                autoreload=True,
        )

        super(WWW, self).__init__(handlers, **settings)


if __name__ == "__main__":
    http_server = HTTPServer(WWW())
    http_server.listen(options.port)
    IOLoop.current().start()
