from rework import api


@api.task
def my_first_task(task):
    with task.capturelogs(std=True):
        print('I am running')
        somevalue = task.input * 2
        task.save_output(somevalue)
        print('I am done')
