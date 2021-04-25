import praw
from wordcloudUtil import *
from get_all_tickers import get_tickers as gt
import requests
import re
import json,urllib.request

reddit = praw.Reddit(
    client_id="VZ3OOz_XrxLXBw",
    client_secret="Gzs5E25-FDqPHQ7F2qDFHf-jBJ72lA",
    username="Puzzleheaded_Row_596",
    password="cs4100project!",
    user_agent="testscript by josh",
)


def tot_sentiment(from_date=str, to_date=str, query=str):
    str1 = "https://api.pushshift.io/reddit/submission/search/?size=100&q="
    str2 = query
    str3 = "&after="
    str4 = from_date
    str5 = "&before="
    str6 = to_date
    str7 = "&sort_type=score&sort=desc&subreddit=wallstreetbets&fields=title"
    url = str1+str2+str3+str4+str5+str6+str7
    print(url)
    source = requests.get(url).json()

    lo_urls = list()
    for post in source['data']:
        lo_urls.append(post['title'].encode('utf-16', 'surrogatepass').decode('utf-16'))
    print(lo_urls)

tot_sentiment("1334426439", "1349696839", "apple")
tot_sentiment("0004426439", "5049696839", "apple")
"""
from datetime import datetime
t = 1523290473.0
dt = datetime.fromtimestamp(t)
print(dt)
"""