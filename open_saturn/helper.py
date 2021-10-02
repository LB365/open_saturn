from inireader import reader
from tshistory_refinery.helper import readsources
from tshistory.api import timeseries


NTHREAD = 16
def config():
    return reader('refinery.ini')
