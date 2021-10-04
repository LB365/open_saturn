import socket
from inireader import reader
from tshistory_refinery.helper import readsources
from tshistory.api import timeseries
import os


def config():
    config = reader('refinery.ini')
    if 'DATABASE_URL' in os.environ.keys() is not None:
        url_env = os.environ['DATABASE_URL'].replace('postgres', 'postgresql')
        config['db']['uri'] = url_env
    return config


def host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]
