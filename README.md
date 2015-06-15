# Tweets Sentiment Analysis

Sentiment analysis on Twitter data has attracted much attention recently. This program is a simple implementation of a sentiment classifier for a tweet. 

Based on the *sentiwordnet* corpus, the classifier can distinguish if a tweet is **Positive**, **Negative**, or **Objective**. 

## Usage 

- To see answers to the TP :  ```python tp.py```
- To see the results of the classification using the first version of the algorithm : ```python tpv1.py```
- To see the results of the classification using the second version of the algorithm :  ```python tpv2.py```
- - To see the results of the classification using the third version of the algorithm :  ```python tpv3.py```

## Requirements 

You need the following libs : 
- sklearn
- nltk
- numpy

## Processing pipeline

The processing pipeline for every tweet is the following : 

### Algorithm v1

- Tweet preprocessing : removal of twitter-specific characters ( mentions : @, hashtags : #, retweets : RT)
- POS tagging : assign every word to its POS tag (Part Of Speech Tag)
- SentiSynset : For words such as adjective, words, nouns, and adverb, find the first sentisynset in the sentiwordnet corpus
- Assign a score for the tweet by aggregating every individual score from the sentisynsets
- Classify the tweet

### Algorithm v2 : taking negation and modifiers into account

- Tweet preprocessing : removal of twitter-specific characters ( mentions : @, hashtags : #, retweets : RT)
- POS tagging : assign every word to its POS tag (Part Of Speech Tag)
- SentiSynset : For words such as adjective, words, nouns, and adverb, find the first sentisynset in the sentiwordnet corpus
- Assign a score for the tweet by aggregating every individual score from the sentisynsets
- Modify the score to take care of negations and modifiers
- Classify the tweet

### Algorithm v3 : taking emojis into account

- Tweet preprocessing : removal of twitter-specific characters ( mentions : @, hashtags : #, retweets : RT)
- POS tagging : assign every word to its POS tag (Part Of Speech Tag)
- SentiSynset : For words such as adjective, words, nouns, and adverb, find the first sentisynset in the sentiwordnet corpus
- Assign a score for the tweet by aggregating every individual score from the sentisynsets
- Modify the score to take care of negations and modifiers
- Increase the positive or negative score by taking care of emojis
- Classify the tweet

# Classify tweets
```
python tpv1.py
```

```
python tpv2.py
```

```
python tpv3.py
```
