import click
import os
import json
from configparser import ConfigParser
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from apscheduler.schedulers.blocking import BlockingScheduler

from rework import api

from open_saturn.helper import config, vacuum


@click.group()
def saturn():
    pass


@saturn.command('template-okta-file')
def generate_okta_secret():
    OKTA_CLIENT_ID = os.environ['OKTA_OAUTH2_CLIENT_ID_WEB']
    OKTA_CLIENT_SECRET = os.environ['OKTA_OAUTH2_CLIENT_SECRET_WEB']
    OKTA_ORG_URL = os.environ['OKTA_CLIENT_ORGURL']
    HOMEPAGE = os.environ['HOMEPAGE']
    secrets = {
        "web": {
            "client_id": f"{OKTA_CLIENT_ID} ",
            "client_secret": f"{OKTA_CLIENT_SECRET}",
            "auth_uri": f"{OKTA_ORG_URL}/oauth2/default/v1/authorize",
            "token_uri": f"{OKTA_ORG_URL}/oauth2/default/v1/token",
            "issuer": f"{OKTA_ORG_URL}/oauth2/default",
            "userinfo_uri": f"{OKTA_ORG_URL}/oauth2/default/userinfo",
            "redirect_uris": [
                f"https://{HOMEPAGE}/oidc/callback"
            ]
        }
    }
    with open('client_secrets.json', 'w') as f:
        json.dump(secrets, f)




@saturn.command('template-config-file')
@click.option('--path', default='refinery.ini')
def replace_uri(path):
    config = ConfigParser()
    config.read(path)
    if 'DATABASE_URL' in os.environ.keys() is not None:
        prefix = 'postgres'
        url = os.environ['DATABASE_URL'].replace(prefix, prefix + 'ql')
        os.environ['REWORKCFGPATH'] = url
        if not config.get('db', 'uri').startswith('postgresql'):
            config.set('db', 'uri', url)
    with open(path, 'w') as configfile:
        config.write(configfile)


@click.command()
def openwebstart():
    from open_saturn.wsgi import app
    app.run(debug=True)


@saturn.command('vacuum')
@click.option('--domain', default='default')
@click.option('--days', type=int, default=7)
def vacuum_now(domain='default', days=7):
    """cleanup the tasks list (for a given domain) of its finished
    tasks (with a default 7 days horizon)
    """
    cfg = config()
    dburi = cfg['db']['uri']
    deleted = vacuum(dburi, domain, horizon=timedelta(days=days))
    print(
        f'deleted {deleted} tasks '
        f'(finished before {datetime.utcnow() - timedelta(days=days)})'
    )


@saturn.command('start-scheduler')
def start_scheduler():
    cfg = config()
    dburi = cfg['db']['uri']
    scheduler = BlockingScheduler()
    scheduler.add_job(
        lambda: vacuum(dburi, 'default'),
        trigger='cron',
        hour='*'
    )
    scheduler.start()


@saturn.command('register-tasks')
@click.option('--cleanup', is_flag=True, default=False)
def register_tasks(cleanup):
    dburi = config()['db']['uri']
    engine = create_engine(dburi)
    from open_saturn import tasks

    if cleanup:
        with engine.begin() as cn:
            cn.execute(
                "delete from rework.operation where path like '%%open_saturn%%'")

    api.freeze_operations(engine)


@saturn.command('schedule-tasks')
def schedule_tasks():
    dburi = config()['db']['uri']
    engine = create_engine(dburi)
    from open_saturn import tasks
    api.prepare(engine, 'my_first_task', '0 0 0 * * *')
