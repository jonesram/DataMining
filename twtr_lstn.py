import sys
import time
import tweepy
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import json
import tweet_tokenizer as tt
from collections import Counter
from nltk import bigrams
from nltk.corpus import stopwords
import string
import pylab as plt
from numpy import *

consumer_key = ""
consumer_secret = ""
access_token_key = ""
access_token_secret = ""

stops = stopwords.words('english') + list(string.punctuation)+['RT','via','amp','...','the']

class listener(StreamListener):
 
   def __init__(self,start_time, time_limit):
      self.time = start_time
      self.limit = time_limit
 
   def on_data(self, data):
      while (time.time() - self.time) < self.limit:
 
         try:
            saveFile = open('raw_tweets.json', 'a')
            saveFile.write(data)
            saveFile.write('\n')
            saveFile.close()
 
            return True
 
         except BaseException, e:
            print 'failed ondata,', str(e)
            time.sleep(5)
            pass
 
      exit()
 
   def on_error(self, status):
      print statuses



def searchTweets(key, start_date, end_date, write = True):
      results = []
    
      for status in tweepy.Cursor(api.search, q=key, since=start_date, until=end_date, lang =  'en').items():
         results.append(json.loads(status.json))
         
      if write:
         ofilename = key.replace(' ','')+'.json'
         with open(ofilename, 'w') as ofile:
            for tweet in results: ofile.write(json.dumps(tweet))
      return results

def searchUsers(key, write = True):
      results = []
      for user in tweepy.Cursor(api.search_users, q=key).items(10):
         results.append(user)
      return results
         

class Tweets(object):

   def __init__(self, j_file = None, tweet_list = None):
      if j_file:
         self.tweets = []
         with open(j_file, 'r') as f:
            for line in f:
               self.tweets.append(json.loads(line))
      if tweet_list:
         self.tweets = tweet_list


 
   def countAll(self):
      count = Counter()
      terms_all = []
      for tweet in self.tweets:
         terms_all += [term for term in tt.preprocess(tweet['text']) if term not in stops]
      count.update(terms_all)
      return count

   def countWords(self):
      count = Counter()
      terms_words = []
      for tweet in self.tweets:
         terms_words += [term for term in tt.preprocess(tweet['text']) if term not in stops and not term.startswith(('#','@'))]
      count.update(terms_words)
      return count

   def countHash(self):
      count = Counter()
      terms_hash = []
      for tweet in self.tweets:
         terms_hash += [term for term in tt.preprocess(tweet['text']) 
              if term.startswith('#')] 
      count.update(terms_hash)
      return count

   def countAt(self):
      count = Counter()
      terms_at = []
      for tweet in self.tweets:
         terms_at += [term for term in tt.preprocess(tweet['text']) 
              if term.startswith('@')] 
      count.update(terms_at)
      return count

   def countBigrams(self):
      count = Counter()
      terms_words = []
      for tweet in self.tweets:
         terms_words += [term for term in tt.preprocess(tweet['text']) if term not in stops and not term.startswith(('#','@'))]
      terms_bigrams = bigrams(terms_words)
      count.update(terms_bigrams)
      return count

def hist(term_counts):
   terms,counts =[],[]
   for  term,count in term_counts: 
      terms.append(str(term))
      counts.append(count)
   indexes = arange(len(terms))
   width = 1.0
   plt.bar(indexes,counts,width)
   plt.xticks(indexes+width*0.5,terms,fontsize = 10)
   plt.show()



auth = OAuthHandler(consumer_key, consumer_secret) #OAuth object
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)

@classmethod
def parse(cls, api, raw):
   status = cls.first_parse(api, raw)
   setattr(status, 'json', json.dumps(raw))
   return status
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
# You need to do it for all the models you need

#To stream:
#start_time = time.time()
#twitterStream = Stream(auth, listener(start_time,time_limit=30)) 
#twitterStream.filter(track='espresso', languages=['en'])
