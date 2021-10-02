from pm_utils.flaskutil import ReverseProxied
from data_hub.helper import config
from data_hub.webapi import make_app

app = make_app(config())
app.wsgi_app = ReverseProxied(app.wsgi_app)