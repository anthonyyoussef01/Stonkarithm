import praw
from wordcloudUtil import *
from get_all_tickers import get_tickers as gt

tickers = ["GME", "AMC", "NIO", "PLTR"]

tickerDictionary = {}

def findTicker(text):
    restOfString = text.partition("$")[2]
    ticker = restOfString.partition(" ")[0]
    if ticker in tickers:
        return ticker
    else:
        return ""

def storeData(text):
    if(len(findTicker(text)) > 0):
        tkr = findTicker(text).upper()
        if tkr in tickerDictionary.keys():
            tickerDictionary[tkr].append(text)
        else:
            tickerDictionary[tkr] = [text]


reddit = praw.Reddit(
    client_id="VZ3OOz_XrxLXBw",
    client_secret="Gzs5E25-FDqPHQ7F2qDFHf-jBJ72lA",
    username="Puzzleheaded_Row_596",
    password="cs4100project!",
    user_agent="testscript by josh",
)
print(reddit.user.me())
# continued from code above
text = []
for submission in reddit.subreddit("wallstreetbets").hot(limit=2):
    storeData(submission.title)
    storeData(submission.selftext)
    submission.comments.replace_more(limit=2)
    for top_level_comment in submission.comments:
        storeData(top_level_comment.body)  # Get top-level comments
        for second_level_comment in top_level_comment.replies:
            storeData(second_level_comment.body)

print(tickerDictionary)
# generate_wordcloud(text)
