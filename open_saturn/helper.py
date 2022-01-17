import socket
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import configparser

from inireader import reader


def config():
    config = configparser.ConfigParser()
    config.read('refinery.ini')
    if 'DATABASE_URL' in os.environ.keys() is not None:
        url_env = os.environ['DATABASE_URL'].replace('postgres', 'postgresql')
        config['db']['uri'] = url_env
    with open('refinery.ini', 'w') as configfile:
        config.write(configfile)
    return config

def generate_okta_secret():
    OKTA_CLIENT_ID = os.environ['OKTA_OAUTH2_CLIENT_ID_WEB']
    OKTA_CLIENT_SECRET = os.environ['OKTA_OAUTH2_CLIENT_SECRET_WEB']
    OKTA_ORG_URL_ISSUER = os.environ['OKTA_OAUTH2_ISSUER']
    HOMEPAGE = os.environ['HOMEPAGE']
    return {
        'web': {
            'client_id': f'{OKTA_CLIENT_ID}',
            'client_secret': f'{OKTA_CLIENT_SECRET}',
            'auth_uri': f'{OKTA_ORG_URL_ISSUER}/v1/authorize',
            'token_uri': f'{OKTA_ORG_URL_ISSUER}/v1/token',
            'issuer': f'{OKTA_ORG_URL_ISSUER}',
            'userinfo_uri': f'{OKTA_ORG_URL_ISSUER}/userinfo',
            'redirect_uris': [
                f'{HOMEPAGE}/oidc/callback'
            ]
        }
    }

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
