import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download([
    "names",
    "stopwords",
    "twitter_samples",
    "averaged_perceptron_tagger",
    "vader_lexicon",
    ])

# nltk.word_tokenize(), a function that splits raw text into individual words
testText = " Josh is writing this because he feels good that he got his vaccination and a internship offer"
# "if w.isalpha()" punctuation counted as words so this filters them out
wordList = nltk.word_tokenize(testText)
words = [ w for w in wordList if w.isalpha()]
text = nltk.Text(words)
fd = nltk.FreqDist(words)
stopwords = nltk.corpus.stopwords.words("english")
words = [w for w in words if w.lower() not in stopwords]
print(words)

sia = SentimentIntensityAnalyzer()
print(sia.polarity_scores(testText))



tweets = [t.replace("://", "//") for t in nltk.corpus.twitter_samples.strings()]

def is_positive(tweet: str) -> bool:
    """True if tweet has positive compound sentiment, False otherwise."""
    return sia.polarity_scores(tweet)["compound"] > 0

# for tweet in tweets[:10]:
#     print(">", is_positive(tweet), tweet)