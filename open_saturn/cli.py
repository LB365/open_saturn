import click

from time import sleep
from rework import api
from sqlalchemy import create_engine

from open_saturn.helper import host, config

@click.command()
def openwebstart():
    from open_saturn.wsgi import app
    app.run(debug=True)

@click.command('register-tasks')
@click.option('--cleanup', is_flag=True, default=False)
def register_tasks():
    dburi = config()['db']['uri']
    engine = create_engine(dburi)

    @api.task
    def my_first_task(task):
        with task.capturelogs(std=True):
            print('I am running')
            somevalue = task.input * 2
            task.save_output(somevalue)
            print('I am done')

    if cleanup:
        with engine.begin() as cn:
            cn.execute(
                "delete from rework.operation where path like '%%open_saturn%%'")

    api.freeze_operations(engine)