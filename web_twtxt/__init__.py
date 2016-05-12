import os

from flask import Flask

from flask_appconfig import HerokuConfig
from flask_bootstrap import Bootstrap

from .frontend import frontend


def create_app(configfile=None):
    app = Flask(__name__)

    HerokuConfig(app, configfile)
    Bootstrap(app)

    app.register_blueprint(frontend)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    app.config['EMBEDLY_KEY'] = os.environ.get('EMBEDLY_KEY')

    app.config['TWTXT_FEED'] = os.environ.get('TWTXT_FEED')
    app.config['TWTXT_NICK'] = os.environ.get('TWTXT_NICK')

    return app


app = create_app()

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port, debug=True)
