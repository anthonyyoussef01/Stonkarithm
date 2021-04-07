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

search_words = "$GME"
date_since = "2018-11-16"

tweets = tw.Cursor(api.search,
              q=search_words + " -filter:retweets",
              lang="en",
              since=date_since).items(5)

tweets = [tweet.text for tweet in tweets]
print(tweets)

