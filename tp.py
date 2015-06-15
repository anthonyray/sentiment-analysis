from msg import *
import os
import csv
import re
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn

from preprocessing import *
from pos_tagging import *
from negation import NegatingWordReader
from modifier import ModifierWordReader


tweets = list()

f = open('testdata.manual.2009.06.14.csv','rt')
concat = ''
try:
    reader = csv.reader(f)
    for row in reader:
        concat += row[5]
        tweets.append(row)
finally:
    f.close()


def is_adjective(tag):
    if tag == 'JJ' or tag == 'JJR' or tag == 'JJS':
        return True
    else:
        return False

def is_adverb(tag):
    if tag == 'RB' or tag == 'RBR' or tag == 'RBS':
        return True
    else:
        return False

def is_noun(tag):
    if tag == 'NN' or tag == 'NNS' or tag == 'NNP' or tag == 'NNPS':
        return True
    else:
        return False

def is_verb(tag):
    if tag == 'VB' or tag == 'VBD' or tag == 'VBG' or tag == 'VBN' or tag == 'VBP' or tag == 'VBZ':
        return True
    else:
        return False

def is_valid(token):
    if is_noun(token[1]) or is_adverb(token[1]) or is_verb(token[1]) or is_adjective(token[1]):
        return True
    else:
        return False


nwr = NegatingWordReader('NegatingWordList.txt')
mwr = ModifierWordReader('BoosterWordList.txt')


def filter_tweet(tweet):
    return map(lambda x : x[0], filter(lambda token : is_valid(token), tweet))

"""
Score calculation functions
"""

def get_sentiment_from_level(i):
    if i == 4:
        return 'Positive'
    elif i == 2:
        return 'Neutral'
    else:
        return 'Negative'

def get_first_synset(word):
    synsets = swn.senti_synsets(word)
    if len(synsets) > 0:
        return synsets[0]
    else:
        return None

def get_synsets(tweet):
    return filter(lambda x: x is not None ,map(lambda x : get_first_synset(x),tweet))

def get_posScore_from_synsets(sentisynsets):
    scores = map(lambda sentisynset: sentisynset.pos_score(), sentisynsets)
    if len(scores) > 0:
        return reduce(lambda a,x: a + x, scores)
    else:
        return 0

def get_negScore_from_synsets(sentisynsets):
    scores = map(lambda sentisynset: sentisynset.neg_score(), sentisynsets)
    if len(scores) > 0:
        return reduce(lambda a,x: a + x, scores)
    else:
        return 0

def get_tweet_sentiment_from_score(posScore, negScore):
    if posScore > negScore:
        return 'Positive'
    elif posScore == negScore:
        return 'Neutral'
    else:
        return 'Negative'

def get_sentiment_from_tweet(tweet):
    tweet = filter_tweet(tweet)
    sentisynsets = get_synsets(tweet)
    posScore = get_posScore_from_synsets(sentisynsets)
    negScore = get_negScore_from_synsets(sentisynsets)

    sentiment = get_tweet_sentiment_from_score(posScore, negScore)

    return posScore, negScore, sentiment

"""
Main
"""

tweets_tagged = map(lambda tweet: pos_tagging(preprocess(tweet,dicoSlang)), tweets)

real_sentiments = map(lambda tweet: get_sentiment_from_level(int(tweet[0])),tweets)
predicted_sentiments = map(lambda tweet: get_sentiment_from_tweet(tweet)[2], tweets_tagged)


import numpy as np
from sklearn.metrics import classification_report

y_true = np.array(real_sentiments)
y_pred = np.array(predicted_sentiments)



print classification_report(y_true,y_pred)

"""
Question 5



question(5)
"""
