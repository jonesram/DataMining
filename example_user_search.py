import twtr_lstn as tl
import json


#perform a user search for 'Caffe Vita' (the coffe shop I happened to be at)
vita_user_search = tl.searchUsers('"Caffe Vita"', write = False)
vita = vita_user_search[0] #I'm feeling lucky

#To double check
print 'User screen name is %s' % vita.screen_name
raw_input("...")

#There's a lot of information in tweepy's user object, a couple examples
print '%s is located in %s' % (vita.screen_name, vita.location)

print '%s has %d follows' % (vita.screen_name, vita.followers_count)

print '%s has posted %d statuses' % (vita.screen_name, vita.statuses_count)
raw_input("...")

#Let's check out their timeline: here are the last couple posts
for status in tl.tweepy.Cursor(tl.api.user_timeline, id = vita.id).items(2): 
   print status.text+'\n'

raw_input("...")

#Let's actually do some analysis!
#First to collect their tweets
tweets = []
for status in tl.tweepy.Cursor(tl.api.user_timeline, id = vita.id).items(100):
   tweets.append(json.loads(status.json))

vita_tweets = tl.Tweets(tweet_list = tweets)

common_words = vita_tweets.countWords().most_common(10)
print 'The 10 most common words are'
for term,count in common_words: print term,count

common_hash = vita_tweets.countHash().most_common(10) 
print 'The 10 most common hash tags are'
for term,count in common_hash: print term,count

common_at = vita_tweets.countAt().most_common(10)
print 'The 10 most common @usernames are'
for term,count in common_at: print term,count

common_bi = vita_tweets.countBigrams().most_common(10)
print 'The 10 most common bigrams are'
for (term1,term2),count in common_bi: print term1,term2,count

raw_input('...')
tl.hist(common_at)

