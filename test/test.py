# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Base:
    def __init__(self):
        self.hello = "world"



class Newone(Base):
    def __init__(self):
        self.name = "new one"
        super(Newone, self).__init__()

    def report(self):
        print self.hello
        print self.name



n = Newone()
n.report()
