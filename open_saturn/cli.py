import click
from time import sleep
from sqlalchemy import create_engine
from apscheduler.schedulers.blocking import BlockingScheduler

from rework import api
from rework.cli import monitor

from open_saturn.helper import host, config, vacuum


@click.group()
def saturn():
    pass


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
