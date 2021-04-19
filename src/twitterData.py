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

def get_tweets():
    count = 1000

    s1 = input("Type ticker ")
    s1 = f"(${s1}"
    s2 = ") min_faves:200 lang:en -filter:links -filter:replies -filter:retweets"
    query = s1 + s2

    # empty list to store parsed tweets
    tweets = []
    target = io.open("mytweets.txt", 'w', encoding='utf-8')

    # call twitter api to fetch tweets
    q=str(query)
    fetched_tweets = api.search(q, lang = 'en', count=count, tweet_mode='extended')

    print(len(fetched_tweets))
    # if we have less than 90 relevant tweets, we will attempt to get more
    if (len(fetched_tweets) < 90):
        s2 = ") min_faves:20 lang:en -filter:links -filter:replies -filter:retweets"
        query = s1 + s2

        # empty list to store parsed tweets
        tweets = []
        target = io.open("mytweets.txt", 'w', encoding='utf-8')

        # call twitter api to fetch tweets
        q = str(query)
        fetched_tweets = api.search(q, lang='en', count=count, tweet_mode='extended')

        print(len(fetched_tweets))
        if (len(fetched_tweets) < 90):
            # Configure
            c = twint.Config()
            c.Search = query
            c.Limit = count
            c.Store_csv = True
            c.Output = "result"
            c.Lang = "en"

            # Run
            twint.run.Search(c)

            # get list of tweets
            colnames = ['num1', 'num2', 'time-zone', 'date', 'time', 'num3', 'num4', 'username', 'tweet']
            data = pandas.read_csv('result/tweets.csv', names=colnames)

            fetched_tweets = data.tweet.tolist()
            print(fetched_tweets)
            """
            # get today's date
            to_date = datetime.today().strftime('%Y-%m-%d')

            # get the date from 2 weeks ago
            twa = datetime.now() - timedelta(14)
            from_date = datetime.strftime(twa, '%Y-%m-%d')

            # use GetOldTweets3 to get older tweets
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query) \
                .setSince(from_date) \
                .setUntil(to_date) \
                .setMaxTweets(count)
            tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
            print(tweet.text)
            """

    # parsing tweets one by one
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

"""
results = []
with open('nasdaq_screener.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        results.append(row[0])
s1 = " OR $".join(results)
s1 = f"(${s1}"
s2 = ") min_faves:200 lang:en -filter:links -filter:replies -filter:retweets"
query = s1+s2
print(query)
"""
tweets = get_tweets()

# convert 'tweets' list to pandas.DataFrame
tweets_df = pd.DataFrame(tweets)
# define file path (string) to save csv file to
FILE_PATH = "C:\\Users\\antho\\PycharmProjects\\Stonkarithim\\src\\result.csv"
# use pandas to save dataframe to csv
tweets_df.to_csv(FILE_PATH)


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