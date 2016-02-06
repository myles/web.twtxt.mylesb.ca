import re

from flask import current_app as app

from embedly import Embedly
from twtxt.parser import parse_iso8601


def get_links(text):
    url_regex = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = url_regex.findall(text)
    
    embedly = []
    
    client = Embedly(app.config['EMBEDLY_KEY'])
    
    for url in urls:
        embedly.append(client.oembed(url))
    
    return embedly

def process_tweet(raw_tweet):
    tweet = {}
    
    parts = raw_tweet.partition('\t')
    tweet['timestamp'] = parse_iso8601(parts[0])
    tweet['text'] = parts[2].lstrip().rstrip()
    tweet['urls'] = get_links(parts[2].lstrip().rstrip())
    
    return tweet
