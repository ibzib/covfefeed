#!/usr/bin/env python
import nltk
import string
import random
import twitter
from getpass import getpass
import ConfigParser
import os

# from https://github.com/bear/python-twitter/blob/master/examples/tweet.py
class TweetRc(object):
    def __init__(self):
        self._config = None

    def GetConsumerKey(self):
        return self._GetOption('consumer_key')

    def GetConsumerSecret(self):
        return self._GetOption('consumer_secret')

    def GetAccessKey(self):
        return self._GetOption('access_key')

    def GetAccessSecret(self):
        return self._GetOption('access_secret')

    def _GetOption(self, option):
        try:
            return self._GetConfig().get('Tweet', option)
        except:
            return None

    def _GetConfig(self):
        if not self._config:
            self._config = ConfigParser.ConfigParser()
            self._config.read(os.path.expanduser('~/.tweetrc'))
        return self._config

def generateText(cfdist, word, max_length=140):
    output = word
    while True:
        choices = []
        if word in cfdist:
            for next_word, freq in cfdist[word].items():
                choices += freq * [next_word]
            word = random.choice(choices)
        else:
            word = random.choice(cfdist.keys())
        suffix = word
        if word not in string.punctuation:
            suffix = ' ' + suffix
        if len(output) + len(suffix) <= max_length:
            output += suffix
        else:
            break
    return output

def generateTweet(tweets):
    tokenizer = nltk.TweetTokenizer()
    texts = map(tokenizer.tokenize, tweets)
    bigrams = []
    for text in texts:
        bigrams += nltk.bigrams(text)
    cfd = nltk.ConditionalFreqDist(bigrams)
    cur_word = random.choice(random.choice(texts))
    print generateText(cfd, cur_word)

def getTwitterApi():
    tweet_rc = TweetRc()
    consumer_key = tweet_rc.GetConsumerKey() or getpass('Enter your Consumer Key: ')
    consumer_secret = tweet_rc.GetConsumerSecret() or getpass('Enter your Consumer Secret: ')
    access_token_key = tweet_rc.GetAccessKey() or getpass('Enter your Access Token: ')
    access_token_secret = tweet_rc.GetAccessSecret() or getpass('Enter your Access Token Secret: ')
    api = twitter.Api(consumer_key=consumer_key,
      consumer_secret=consumer_secret,
      access_token_key=access_token_key,
      access_token_secret=access_token_secret)
    return api

print 'Generating tweet...\n'
api = getTwitterApi()
# TODO get a larger collection of tweets
tweets = [s.text for s in api.GetUserTimeline(screen_name='@realDonaldTrump')]
message = generateTweet(tweets)
print ''
response = raw_input('Tweet this? (y/N)\n')
if response == 'y' or response == 'Y' or response == 'yes':
    api.PostUpdate(message)
