import requests

from tshistory.api import timeseries as _timeseries


def timeseries(url, token):
    with requests.Session() as s:
        secure_header = {'Authorization': f'token {token}'}
        s.headers.update(secure_header)
        return _timeseries(url)
