import os
from tshistory_refinery.wsgi import app

from open_saturn.helper import config
from open_saturn.webapi import make_okta_app, make_open_app

types = {
    'dev': make_open_app,
    'prd': make_okta_app,
}
config_ = config()
print(config_.__dict__)
app_type = os.environ['APP_TYPE']
app = types[app_type](app)
