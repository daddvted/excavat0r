# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime


class Waiter:
    def get_time(self, lang="cn"):
        if lang == "cn":
            now = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        else:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return now
