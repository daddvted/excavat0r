# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .Element import Element

import os.path
import jieba
import jieba.posseg
import nltk


class SemanticMan(Element):
    def __init__(self):
        super(SemanticMan, self).__init__()

    def extract_spo(self, sentence):
        jieba.load_userdict(os.path.join(self.base_path, "dat/self_idf.txt"))
        pairs = jieba.posseg.cut(sentence)

        prepared_sentence = []
        for w, t in pairs:
            prepared_sentence.append((w, t))

        grammar = r"""
            SUB:
                {^<j|n|ng|nr|ns|nt|nz|r|x>+.*}
            PRE:
                {.*<v|vd|vg|vn>+.*}
            OBJ:
                {.*<j|n|nr|x>+$}
            ADV:
                {.*<p|r>+}
        """
        parser = nltk.RegexpParser(grammar)
        result = parser.parse(prepared_sentence)
        # result.draw()

        extraction = {}
        for r in result:
            if isinstance(r, nltk.tree.Tree):
                phrase = ""
                for leaf in r.leaves():
                    phrase += leaf[0]
                extraction[r.label()] = phrase
        return extraction
