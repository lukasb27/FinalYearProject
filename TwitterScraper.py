import tweepy
import json
from keys import *
import tweepy, time
from datetime import datetime
# Specify the account credentials in the following variables:




def get_tweets():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    username = 'lukasball27'

    api = tweepy.API(auth)

    now = datetime.now()
    now = now.strftime('%Y-%m-%d')
    # print(datetime.now())
    # # print("Today's date: ", now.strftime('%Y-%m-%d'))
    # print(now)

    page = 1
    deadend = False
    while True:
        tweets = api.user_timeline(username, page = page)

        for tweet in tweets:
            lol  = tweet.created_at
            lol = lol.strftime('%Y-%m-%d')
            # print('this is a laugh', lol)
            if now == lol:

                #Do processing here:
                list = ['test', 'blah', 'foo', 'foobar', 'word', 'bad']
                # print(now, tweet.created_at)
                for i in list:
                    if i in tweet.text.lower():
                        print(tweet.text)
                        return True
            else:
                deadend = True
                return False

        if not deadend:
            page+=1
            time.sleep(500)
            return





get_tweets()