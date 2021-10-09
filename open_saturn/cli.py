import click

from time import sleep
from rework import api
from sqlalchemy import create_engine

from open_saturn.helper import host, config

@click.group()
def saturn():
    pass


@click.command()
def openwebstart():
    from open_saturn.wsgi import app
    app.run(debug=True)


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
