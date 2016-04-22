# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path


class Element(object):

    def __init__(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.path.dirname(file_path)
