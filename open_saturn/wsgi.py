from pm_utils.flaskutil import ReverseProxied
from open_saturn.helper import config
from open_saturn.webapi import make_open_app
import os


heroku_app = make_open_app(config(os.environ['DATABASE_URL']))
app = make_open_app(config())
app.wsgi_app = ReverseProxied(app.wsgi_app)
heroku_app.wsgi_app = ReverseProxied(app.heroku_app)