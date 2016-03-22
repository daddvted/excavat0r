import tornado.web

# from .Util import *
# from .Core import *


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", people="skipper")

