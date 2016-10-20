import os
import sys
import logging.config
from configparser import ConfigParser

import tornado.web
import tornado.httpserver
import tornado.ioloop

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("heatmap.html")

class Simple(tornado.web.Application):
    def __init__(self):
        base_path = os.path.dirname(__file__)

        handlers = [
            # (r"/api_cq/debug", DebugHandler),

            # Service API with crawled data
            (r"/", IndexHandler),

        ]

        settings = dict(
            template_path=base_path,
            static_path=base_path,
            # upload_path=os.path.join(os.path.dirname(__file__), "upload"),
            # config_path=os.path.join(os.path.dirname(__file__), "conf"),
            xsrf_cookies=False,
            cookie_secret="__WITH_GREAT_POWER_COMES_GREAT_RESPONSIBILITY__",
            debug=True,
            autoreload=False,
        )

        super().__init__(handlers, **settings)


if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 8080
    http_srv = tornado.httpserver.HTTPServer(Simple())
    http_srv.listen(port)
    tornado.ioloop.IOLoop.current().start()
