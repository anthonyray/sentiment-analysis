from msg import *
import os
import csv
import re
import nltk
from nltk.corpus import wordnet as wn

from preprocessing import *
from pos_tagging import *
from negation import NegatingWordReader
from modifier import ModifierWordReader

welcome_msg()

"""
Reading tweets
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

from nltk.corpus import wordnet as wn
from sentiwordnet import *

swn = SentiWordNetCorpusReader('SentiWordNet_3.0.0_20130122.txt')
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
    synsets = wn.synsets(word)
    if len(synsets) > 0:
        return synsets[0].name().encode('utf8')
    else:
        return None

def get_synsets(tweet):
    return filter(lambda x: x is not None ,map(lambda x : get_first_synset(x),tweet))

def get_sentisynsets(synsets):
    return filter(lambda x : x is not None, map(lambda synset : swn.senti_synset(synset), synsets))

def tweet_has_negation(tweet):
    dweebs = map(lambda x : nwr.has_negation(x[0]),tweet)
    return reduce(lambda a,x: a or x , dweebs )

def find_previous_word_from_tweet(tweet,word):
    tweet = map(lambda x : x[0], tweet)
    try:
        index = tweet.index(word)
        if index > 0:
            return tweet[index - 1]
        else:
            return None
    except ValueError:
            return None

def get_posScore_from_synsets(sentisynsets,tweet):
    """
    Second version of score calculation. It implements the following rules :
        - If the word is a modifier : multiply the positive score by two for the sentisynset
        - Only use the negative score of the word for the global positive score

    First, determine the presence of a negation
    Second, determine a list of sentisynsets that are preceded by a modifier
    Third, calculate the score

    """
    tweet_has_negation_word = tweet_has_negation(tweet) # 1.
    if tweet_has_negation_word:

    else:
        posScore = 0
        for sentisynset in sentisynsets:
            word = sentisynset.get_word()
            previous_word = find_previous_word_from_tweet(tweet,word)
            if mwr.has_modifier(previous_word):
                posScore = posScore + 2 * sentisynset.posScore
            else:
                posScore = posScore + sentisynset.posScore


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
    posScore = get_posScore_from_synsets(sentisynsets,tweet)
    #negScore = get_negScore_from_synsets(sentisynsets)

    #sentiment = get_tweet_sentiment_from_score(posScore, negScore)

    return posScore#, negScore, sentiment

tweets_tagged = map(lambda tweet: pos_tagging(preprocess(tweet,dicoSlang)), tweets)

predicted_sentiments = map(lambda tweet: get_sentiment_from_tweet(tweet)[0], tweets_tagged)
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

question(6)

question(7)
