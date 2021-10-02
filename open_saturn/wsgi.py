from pm_utils.flaskutil import ReverseProxied
from open_saturn.helper import config
from open_saturn.webapi import make_open_app

app = make_open_app(config())
app.wsgi_app = ReverseProxied(app.wsgi_app)