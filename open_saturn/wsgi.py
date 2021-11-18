import os
from pm_utils.flaskutil import ReverseProxied
from open_saturn.helper import config
from open_saturn.webapi import make_okta_app, make_open_app

app_type = {
    'dev': make_open_app,
    'prd': make_okta_app,
}

app = app_type[os.environ['APP_TYPE']](config())
#app.wsgi_app = ReverseProxied(app.wsgi_app)
