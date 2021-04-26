# use "pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint"
import twint

def get_tweets(from_date=str, query=str):
    c = twint.Config()
    c.Search = query
    c.Limit = 100
    c.Since = from_date
    c.Lang = "en"
    c.Min_likes = 10
    c.Links = "exclude"
    c.Pandas = True
    c.Hide_output = True
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    tweet_list = []
    if not Tweets_df.empty:
        Tweets_df = Tweets_df[['date', 'tweet']]
        # print("tweets_found", len(Tweets_df.values))
        for date, tweet in Tweets_df.values:
            # if from_date in date:
            tweet_list.append(tweet)
    return tweet_list
