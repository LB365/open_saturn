from rework import api


@api.task(inputs=())
def my_first_task(task):
    with task.capturelogs(std=True):
        print('I am running')
        print('I am done')
