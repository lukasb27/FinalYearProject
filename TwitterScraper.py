from keys import *
import tweepy
from datetime import datetime


def get_tweets():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    username = 'lukasball27'

    api = tweepy.API(auth)

    now = datetime.now()
    now = now.strftime('%Y-%m-%d')

    while True:
        tweets = api.user_timeline(username)

        for tweet in tweets:
            tweetCreatedDate  = tweet.created_at
            tweetCreatedDate = tweetCreatedDate.strftime('%Y-%m-%d')
            if now == tweetCreatedDate:

                # Do processing here:
                keyWords = ['bad day', 'rubbish day', 'stressed', 'anxious', 'depressed', 'panic attack']
                for i in keyWords:
                    if i in tweet.text.lower():
                        return True
            else:
                return False

get_tweets()