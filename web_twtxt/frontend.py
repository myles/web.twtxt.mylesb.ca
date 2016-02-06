import logging
import requests

from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    current_app as app
)

from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION

from .utils import process_tweet

logger = logging.getLogger(__name__)
frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    raw_tweets = requests.get(app.config['TWTXT_FEED']).text
    
    tweets = []
    
    for raw_tweet in raw_tweets.split('\n')[:-1]:
        try:
            tweets.append(process_tweet(raw_tweet))
        except (ValueError, OverflowError) as e:
            logger.debug(e)
    
    return render_template('index.html', tweets=reversed(tweets))
