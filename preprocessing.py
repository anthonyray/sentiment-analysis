import nltk
import re
import regexes as regexes

def load_slang():
    slangdict = dict()
    with open('slanglookup.txt','rt') as f:
        for line in f:
            spl = line.split('\t')
            slangdict[spl[0]] = spl[1][:-1]
    return slangdict

dicoSlang = load_slang()

def remove_urls(txt):
    """
    Input
    -----
        - a string
    Output
    ------
        - a cleaned string
    """
    tokens = txt.split(' ')
    clean_string = ''
    for token in tokens:
        match = re.search(regexes.URL_REGEX,token)
        if not match:
            clean_string += token + ' '

    return clean_string


def remove_tweet_specific_chars(tokens):
    """
    Input
    -----
        - list of tokens
    Output
    ------
        - list of cleaned tokens

    """

    return [ token for token in tokens if token !='@' and token != '#' and token !='RT' ]


def replace_slang(tokens,dicoSlang):
    return [token if not dicoSlang.has_key(token) else dicoSlang[token] for token in tokens ]


def preprocess(tweet, dicoSlang):
    """
    Input
    -----

        - tweet : a string of words
        - dicoSlang : dictionnary which links abbreviations and their relative words

    Output
    ------
        - preProcessedTweet = list of words

    Algorithm
    ---------

        1. Retrieve text
        2. Tokenize the text
        3. Remove urls
        4. Clean tweet specific characters
        5. Correct abbreviations and use dicoSlang

    """

    tweet_text = tweet[5] # 1. Retrieve text

    tweet_url_cleaned = remove_urls(tweet_text) # 3. Remove urls
    tokens = nltk.word_tokenize(tweet_url_cleaned) # 2. Tokenize the text
    tokens = remove_tweet_specific_chars(tokens)
    tokens = replace_slang(tokens,dicoSlang)
    return tokens
