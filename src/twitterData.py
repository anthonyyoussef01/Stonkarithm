import io
import tweepy
import re
import csv
import pandas as pd
from stockData import *

consumer_key = 'sz6x0nvL0ls9wacR64MZu23z4'
consumer_secret = 'ofeGnzduikcHX6iaQMqBCIJ666m6nXAQACIAXMJaFhmC6rjRmT'
access_token = '854004678127910913-PUPfQYxIjpBWjXOgE25kys8kmDJdY0G'
access_token_secret = 'BC2TxbhKXkdkZ91DXofF7GX8p2JNfbpHqhshW1bwQkgxN'
# create OAuthHandler object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# set access token and secret
auth.set_access_token(access_token, access_token_secret)
# create tweepy API object to fetch tweets
api = tweepy.API(auth)

# create list to append tweets to
tweets = []
TICKER = '$GME'

def get_tweets(query, count):
    # empty list to store parsed tweets
    tweets = []
    target = io.open("mytweets.txt", 'w', encoding='utf-8')

    # call twitter api to fetch tweets
    q=str(query)
    fetched_tweets = api.search(q, lang = 'en', count=count, tweet_mode='extended')

    # parsing tweets one by one
    print(len(fetched_tweets))

    for tweet in fetched_tweets:
        # empty dictionary to store required params of a tweet
        parsed_tweet = {}
        # saving text of tweet
        parsed_tweet['text'] = tweet.full_text

        #filter the words in the tweets
        #line = re.sub("[^A-Za-z]", " ", tweet.text)
        #target.write(line+"\n")
        line = re.sub('@[\w]+', '', tweet.full_text)
        target.write(line+"\n")
        target.write("--------------------------------------------------------------\n")
        # append all tweet data to list
        tweets.append(line)
    return tweets

def buildTweetDataFrame(startDate, endDate):
    query = TICKER + " -filter:links -filter:replies -filter:retweets"
    start = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    end = datetime.datetime.strptime(endDate, "%Y-%m-%d")
    # fetched_tweets = api.search(query, lang='en', count=100, until=end)
    fetched_tweets = tweepy.Cursor(api.search,
                                   query,
                                   lang="en",
                                   until=end,
                                   result_type="recent")
    print(fetched_tweets.items().num_tweets)
    for tweet_info in fetched_tweets.items():
        date = tweet_info.created_at.date()
        print(date)
        text = tweet_info.full_text
        price = getStockPrice(date,TICKER)
        data = pd.DataFrame(data = [date,text,price], columns=['Date','Tweets', 'Price'])
    return data


tData = buildTweetDataFrame('2021-4-12', '2020-4-13')
print(tData)

# results = []
# with open('nasdaq_screener.csv', newline='') as inputfile:
#     for row in csv.reader(inputfile):
#         results.append(row[0])
# s1 = " OR $".join(results)
# s1 = f"(${s1}"
# s2 = ") min_faves:200 lang:en -filter:links -filter:replies -filter:retweets"
# query = s1+s2
# print(query)
#
# tweets = get_tweets(query=query, count=20000)
# print(tweets);
#
# # convert 'tweets' list to pandas.DataFrame
# tweets_df = pd.DataFrame(tweets)
# # define file path (string) to save csv file to
# FILE_PATH = "C:\\Users\\antho\\PycharmProjects\\Stonkarithim\\src\\result.csv"
# # use pandas to save dataframe to csv
# tweets_df.to_csv(FILE_PATH)


"""
api_key= 'KrFweRtE6JBhzTjPqoU5jaBuR'
api_secret= 'YDxrQ4T9qYP6uUpRru3UFWmhTuKT0mMGx1Kmj0dMtYFwmtssQA'
bearer_token= 'AAAAAAAAAAAAAAAAAAAAAI2IOQEAAAAAk971Tpb%2BoCzTPjJHQWS6snjVBww%3Da6Y3iJLl8SwaUNjNTCmUvczugx5i37ERQewpc1SFTkLtMJ22HW'
access_token= '822570826985828352-sfrlzDWAYqJtyHFZGVT405fHr9G8q4E'
access_token_secret= 'WOcNAC0h8Hcr2OGnDm4UK9JkRaiFIwXFK4tvER8RHiOrD'

import tweepy as tw
import pandas as pd

auth = tw.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = ["$GME", "$AMC"]
date_since = "2018-11-16"

tweets = tw.Cursor(api.search,
              q=search_words + " -filter:retweets",
              lang="en",
              since=date_since).items(20)

tweets = [tweet.text for tweet in tweets]
print(tweets)
"""