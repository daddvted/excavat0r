# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path
import jieba
import jieba.posseg
import nltk

from .Element import Element


class SemanticMan(Element):
    def __init__(self):
        super(SemanticMan, self).__init__()

    def analyze_structure(self, sentence):
        jieba.load_userdict(os.path.join(self.base_path, self.dict_file))
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

        structure = {}
        for r in result:
            if isinstance(r, nltk.tree.Tree):
                # phrase = ""
                phrase = []
                for leaf in r.leaves():
                    # phrase += leaf[0]
                    phrase.append(leaf[0])
                structure[r.label()] = phrase
        return structure
        # 'structure' looks like
        # {
        #   'SUB':["我"],
        #   'PRE':["想","查询"],
        #   'OBJ':["天气"],
