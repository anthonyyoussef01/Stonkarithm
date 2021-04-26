import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from statistics import mean
from twitterData import get_tweets
import pandas as pd

nltk.download(["vader_lexicon"])

sia = SentimentIntensityAnalyzer()
# add meme works and other financial terms, and how we should rate them in regards to sentiment
# common words range from -3 to 3 so weight these a little more
stock_meme_words = {
    'moon': 4.0,
    'mooning': 4.0,
    'DD': 2.8,
    'BTFD': -2.8,
    'mars': 0.5,
    'tendies': 3.5,
    'rocket': 2.5,
    'hold': -2.5,
    'diamond': -2.0,
    'paper': -3.0,
    'yolo': 1.0,
    'f': -4.8,
    'sold': -3.0,
    'sell': -3.0,
    'buy': 2.5,
    'buying': 2.5,
    'bought': 2.5,
    'pullback': -4.0,
    'bullish': 3.8,
    'bearish': -3.8,
    'dip': -4.0,
    '🚀': 3.0,
    '💎': 1.5,
    '📈': 3.0,
    '📉': -3.0
}
sia.lexicon.update(stock_meme_words)

# test different phrases
#test = ["gme to the moon","All in Apple", "Sold all my apple and bought more in GME", "Message from a TSLA veteran: Shut the fuck up and hold", "I hate apple"]

def getTwitterSentimentScore(dateList):
    sentiment = []
    for date in dateList:
        t = pd.to_datetime(str(date))
        dateStr = t.strftime("%Y-%m-%d")
        listOfTweets = get_tweets(dateStr)
        scores = []
        for text in listOfTweets:
            cmp = sia.polarity_scores(text)["compound"]
            scores.append(cmp)
        if len(scores) > 0:
             sentiment.append(mean(scores))
        else:
            sentiment.append(0)
    return sentiment




