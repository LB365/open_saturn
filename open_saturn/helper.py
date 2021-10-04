import socket
from inireader import reader
from tshistory_refinery.helper import readsources
from tshistory.api import timeseries

NTHREAD = 16


def config():
    if 'DATABASE_URL' in os.environ.keys() is not None:
        config = reader('refinery-heroku.ini')
        config['db']['uri'] = os.environ['DATABASE_URL'].replace('postgres',
                                                                 'postgresql')
        return config
    else:
        return reader('refinery.ini')


def host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]
