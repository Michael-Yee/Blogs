from proj.celery import app
from proj.celeryconfig import A_QUEUE, M_QUEUE, S_QUEUE
from time import sleep


@app.task(bind=True, name='proj.tasks.add', queue=A_QUEUE, default_retry_delay=1, max_retries=3)
def add(self, x, y):
    try:
        return x + y
    except Exception as exc:
        raise self.retry(exc=exc)


@app.task(name='proj.tasks.mul', queue=M_QUEUE)
def mul(x, y):
    sleep(5)
    return x * y


@app.task(bind=True, name='proj.tasks.square', queue=S_QUEUE, default_retry_delay=1, max_retries=1)
def square(self, x):
    try:
        return mul(x=x, y=x)
    except Exception as exc:
        raise self.retry(exc=exc)
