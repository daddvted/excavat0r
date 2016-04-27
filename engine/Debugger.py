# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .TextMan import TextMan
from .SemanticMan import SemanticMan


class Debugger:
    def __init__(self):
        self.textman = TextMan()
        self.semanticman = SemanticMan()

        self.response_code = ""
        self.response = None

    # Receive dict and return dict
    def debug_routing(self, message):
        code = message["code"]
        msg = message["msg"]

        # segment
        if code == '901':
            self.response_code = "901"
            self.response = TextMan.segment(msg)
            return self._send_debug_response()
        # segment for search
        elif code == '904':
            self.response_code = "904"
            self.response = TextMan.segment_for_search(msg)
            return self._send_debug_response()
        # keywords extraction
        elif code == '902':
            self.response_code = "902"
            self.response = " | ".join(self.textman.extract_keyword(msg))
            return self._send_debug_response()
        # extract sentence structure
        elif code == '905':
            self.response_code = "905"
            self.response = self.semanticman.analyze_structure(msg)
            return self._send_debug_response()
        # word flag
        elif code == '903':
            flags = TextMan.tag(msg)
            resp_list = []
            for word, flag in flags:
                resp_list.append({
                    "word": word,
                    "flag": flag,
                })
            self.response_code = "903"
            self.response = resp_list
            return self._send_debug_response()

    def _send_debug_response(self):
        # print "[ MessageRouter.py - _send_response()]", response_code, response
        return {"code": self.response_code, "resp": self.response}
