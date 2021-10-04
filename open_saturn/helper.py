import socket
from inireader import reader
from tshistory_refinery.helper import readsources
from tshistory.api import timeseries


NTHREAD = 16
def config(heroku_url=None):
    if heroku_url is not None:
        config = reader('refinery-heroku.ini')
        config['db']['uri'] = heroku_url
        return config
    else:
        return reader('refinery.ini')

def host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]
