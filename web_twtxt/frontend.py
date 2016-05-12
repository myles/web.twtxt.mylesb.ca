import logging
import requests
from operator import itemgetter

from flask import (
    Blueprint,
    render_template,
    request,
    current_app as app
)

from .utils import process_tweet

logger = logging.getLogger(__name__)
frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    if request.args.get('feed') or request.args.get('nick'):
        twtxt_nick = request.args.get('nick')
        twtxt_feed = request.args.get('feed')
    else:
        twtxt_nick = app.config['TWTXT_NICK']
        twtxt_feed = app.config['TWTXT_FEED']

    r = requests.get(twtxt_feed)

    raw_tweets = r.text

    tweets = []

    for raw_tweet in raw_tweets.split('\n')[:-1]:
        try:
            tweets.append(process_tweet(raw_tweet))
        except (ValueError, OverflowError) as e:
            logger.debug(e)

    tweets.sort(key=itemgetter('timestamp'), reverse=True)

    return render_template('index.html', tweets=tweets,
                           twtxt_nick=twtxt_nick, twtxt_feed=twtxt_feed)
