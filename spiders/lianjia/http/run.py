import os
import sys

import tornado.web
import tornado.httpserver
import tornado.ioloop


class Index(tornado.web.RequestHandler):
    def get(self):
        self.render("heatmap_amap.html")


class Addr2coordBaidu(tornado.web.RequestHandler):
    def get(self):
        self.render("addr2coord_baidu.html")


class Addr2coordAmap(tornado.web.RequestHandler):
    def get(self):
        self.render("addr2coord_amap.html")


class Simple(tornado.web.Application):
    BASE_PATH = os.path.dirname(__file__)

    def __init__(self):

        handlers = [
            (r"/", Index),
            (r"/addr2coordbaidu", Addr2coordBaidu),
            (r"/addr2coordamap", Addr2coordAmap),
        ]

        settings = dict(
            template_path=os.path.join(self.BASE_PATH, "template"),
            static_path=os.path.join(self.BASE_PATH, "static"),
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
