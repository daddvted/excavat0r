# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import nltk
from nltk.corpus import brown

suffix_fdist = nltk.FreqDist()
for word in brown.words():
    word = word.lower()
    suffix_fdist[word[-1:]] += 1
    suffix_fdist[word[-2:]] += 1
    suffix_fdist[word[-3:]] += 1

common_sufix = suffix_fdist.keys()[:50]


def pos_features(word):
    features = {}
    for suffix in common_sufix:
        features['endswith(%s)' % suffix] = word.lower().endswith(suffix)
    return features


tagged_words = brown.tagged_words(categories='news')
print tagged_words
