import praw
import requests


# reddit = praw.Reddit(
#     client_id="VZ3OOz_XrxLXBw",
#     client_secret="Gzs5E25-FDqPHQ7F2qDFHf-jBJ72lA",
#     username="Puzzleheaded_Row_596",
#     password="cs4100project!",
#     user_agent="testscript by josh",
# )


def getRedditPosts(from_date=str, to_date=str, query=str):
    str1 = "https://api.pushshift.io/reddit/submission/search/?size=100&q="
    str2 = query
    str3 = "&after="
    str4 = from_date
    str5 = "&before="
    str6 = to_date
    str7 = "&sort_type=score&sort=desc&subreddit=wallstreetbets&fields=title"
    url = str1+str2+str3+str4+str5+str6+str7
    source = requests.get(url).json()

    list_of_text = list()
    for post in source['data']:
        list_of_text.append(post['title'].encode('utf-16', 'surrogatepass').decode('utf-16'))
    return list_of_text

"""
from datetime import datetime
t = 1523290473.0
dt = datetime.fromtimestamp(t)
print(dt)
"""
