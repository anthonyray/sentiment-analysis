from msg import *
import os
import csv
import re
import nltk
from nltk.corpus import wordnet as wn

from preprocessing import *
from pos_tagging import *

welcome_msg()

"""
Question 1

"""
question(1)

"""
Question 2

Precisez le nombre d'occurences des hash-tags dans le corpus de tweets fourni
"""
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

"""
Question 2
"""

question(2)
print "Il y a ", concat.count('#'), " occurences de hashtags"

"""
Pre-processing
"""

tokens = preprocess(tweets[38],dicoSlang)

"""
Etiquetage grammatical
"""

#print pos_tagging(tokens)


"""
Question 3

Comptez le nombre de mots etiquetes verbes presents dans les tweets
"""
"""
Tweet filters
"""
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


cpt = 0
for tweet in tweets:
    for token in pos_tagging(preprocess(tweet,dicoSlang)):
        if is_verb(token[1]):  # TODO : Take into account all verbal forms
            cpt += 1

question(3)
print 'Il y a : ' + str(cpt) + ' verbes dans la base des tweets'

"""
Question 4

Algorithme de detection v1 : appel au dictionnaire Sentiwordnet
"""

question(4)

from nltk.corpus import wordnet as wn
from sentiwordnet import *

wn.synsets('dog')


swn = SentiWordNetCorpusReader('SentiWordNet_3.0.0_20130122.txt')



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
    synsets = wn.synsets(word)
    if len(synsets) > 0:
        return synsets[0].name().encode('utf8')
    else:
        return None

def get_synsets(tweet):
    return filter(lambda x: x is not None ,map(lambda x : get_first_synset(x),tweet))

def get_sentisynsets(synsets):
    return filter(lambda x : x is not None, map(lambda synset : swn.senti_synset(synset), synsets))

def get_posScore_from_synsets(sentisynsets):
    scores = map(lambda sentisynset: sentisynset.PosScore, sentisynsets)
    if len(scores) > 0:
        return reduce(lambda a,x: a + x, scores)
    else:
        return 0

def get_negScore_from_synsets(sentisynsets):
    scores = map(lambda sentisynset: sentisynset.NegScore, sentisynsets)
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
    synsets = get_synsets(tweet)
    sentisynsets = get_sentisynsets(synsets)
    posScore = get_posScore_from_synsets(sentisynsets)
    negScore = get_negScore_from_synsets(sentisynsets)

    sentiment = get_tweet_sentiment_from_score(posScore, negScore)

    return posScore, negScore, sentiment

tweets_tagged = map(lambda tweet: pos_tagging(preprocess(tweet,dicoSlang)), tweets)

predicted_sentiments = map(lambda tweet: get_sentiment_from_tweet(tweet)[2], tweets_tagged)
real_sentiments = map(lambda tweet: get_sentiment_from_level(int(tweet[0])),tweets)

import numpy as np
from sklearn.metrics import classification_report

y_true = np.array(real_sentiments)
y_pred = np.array(predicted_sentiments)



print classification_report(y_true,y_pred)

"""
Question 5


"""
question(5)
