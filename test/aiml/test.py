# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import aiml
print __file__

k = aiml.Kernel()
k.learn("std_startup.xml")
k.respond("load_aiml")
while True:
    print k.respond(raw_input("> "))
