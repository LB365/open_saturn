import os
from tshistory_refinery.wsgi import ReverseProxied
from open_saturn.helper import config
from open_saturn.webapi import make_okta_app, make_open_app

types = {
    'dev': make_open_app,
    'prd': make_okta_app,
}

conf = config()
print(conf)
app_type = os.environ['APP_TYPE']
app = types[app_type](conf)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.wsgi_app = ReverseProxied(app.wsgi_app)
