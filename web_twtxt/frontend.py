import logging
import requests

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
    r = requests.get(request.args.get('feed', app.config['TWTXT_FEED']))

    raw_tweets = r.text

    tweets = []

    for raw_tweet in raw_tweets.split('\n')[:-1]:
        try:
            tweets.append(process_tweet(raw_tweet))
        except (ValueError, OverflowError) as e:
            logger.debug(e)

    return render_template('index.html', tweets=reversed(tweets))
