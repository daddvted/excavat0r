# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import random
import nltk
from nltk.corpus import names
from nltk.classify.util import apply_features


def gender_features(name):
    return {'last_letter': name[-1]}

def gender_features2(name):
    features = {}
    features['firstletter'] = name[0].lower()
    features['lastletter'] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count(%s)" % letter] = name.lower().count(letter)
        features["has(%s)" % letter] = (letter in name.lower())
    return features


names = ([(name, 'male') for name in names.words('male.txt')] +
         [(name, 'female') for name in names.words('female.txt')])
random.shuffle(names)

# feature_sets = [(gender_features(n), g) for (n, g) in names]
# train_set, test_set = feature_sets[500:], feature_sets[:500]

train_names = names[1500:]
dev_names = names[500:1500]
test_names = names[:500]

train_set = apply_features(gender_features, train_names)
dev_set = apply_features(gender_features, dev_names)
test_set = apply_features(gender_features, test_names)

classifier = nltk.NaiveBayesClassifier.train(train_set)

print classifier.classify(gender_features('Neo'))
print classifier.classify(gender_features('Miya'))
print nltk.classify.accuracy(classifier, test_set)

errors = []
for (name, tag) in dev_names:
    guess = classifier.classify(gender_features(name))
    if guess != tag:
        errors.append((tag, guess, name))

for (tag, guess, name) in sorted(errors):
    print 'correct=%-8s guess=%-8s name=%-30s' %(tag, guess, name)

