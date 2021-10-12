import socket
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine

from inireader import reader
from tshistory_refinery.helper import readsources
from tshistory.api import timeseries


def config():
    config = reader('refinery.ini')
    if 'DATABASE_URL' in os.environ.keys() is not None:
        url_env = os.environ['DATABASE_URL'].replace('postgres', 'postgresql')
        config['db']['uri'] = url_env
    return config


def vacuum(dburi,
           domain='default',
           opname=None,
           horizon=timedelta(days=7)):
    morewhere = ''
    if opname:
        morewhere = 'and op.name = %(opname)s'
    sql = (
        f'with deleted as '
        f'(delete from rework.task as t '
        f'   using rework.operation as op '
        f'   where t.status = \'done\' and '
        f'         t.finished < %(finished)s and '
        f'         op.id = t.operation and '
        f'         op.domain = %(domain)s '
        f'         {morewhere} '
        f' returning 1) '
        f'select count(*) from deleted'
    )
    finished = datetime.utcnow() - horizon
    engine = create_engine(dburi)
    with engine.begin() as cn:
        count = cn.execute(
            sql,
            finished=finished,
            domain=domain,
            opname=opname
        ).scalar()
    return count


def host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]
