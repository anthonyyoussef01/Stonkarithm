import io
import tweepy
import re
import csv
import pandas as pd
import GetOldTweets3 as got
from datetime import datetime, timedelta
# use "pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint"
import twint
import pandas

from sentimentAnalysis import sentiment_anal

def tot_sentiment(from_date=str, to_date=str, query=str):
    c = twint.Config()
    c.Search = query
    c.Limit = 100
    c.Since = from_date
    c.Until = to_date
    c.Lang = "en"
    c.Min_likes = 20
    c.Links = "exclude"
    c.Pandas = True
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df

    tweet_list = Tweets_df.tweet.tolist()
    print(tweet_list)


    #print(sentiment_anal(tweet_list))

tot_sentiment("2021-4-21", "2021-4-23", "amc")