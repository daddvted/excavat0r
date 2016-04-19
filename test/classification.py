# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import random
import nltk
from nltk.corpus import names
from nltk.classify import apply_features


def gender_features(word):
    return {'last_letter': word[-1]}


names = ([(name, 'male') for name in names.words('male.txt')] +
         [(name, 'female') for name in names.words('female.txt')])
random.shuffle(names)

# feature_sets = [(gender_features(n), g) for (n, g) in names]
# train_set, test_set = feature_sets[500:], feature_sets[:500]

train_set = apply_features(gender_features, name[500:])
test_set = apply_features(gender_features, name[:500])

classifier = nltk.NaiveBayesClassifier.train(train_set)

print classifier.classify(gender_features('Neoia'))
print classifier.classify(gender_features('Miya'))
print nltk.classify.accuracy(classifier, test_set)
print classifier.show_most_informative_features(5)
