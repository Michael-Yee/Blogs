from proj.celery import app
from proj.celeryconfig import A_QUEUE, M_QUEUE
import time


@app.task(bind=True, name='proj.tasks.add', queue=A_QUEUE, default_retry_delay=1, max_retries=3)
def add(self, x, y):
    try:
        print(x+y)
        return x + y
    except Exception as exc:
        raise self.retry(exc=exc)


@app.task(name='proj.tasks.mul', queue=M_QUEUE)
def mul(x, y):
    print('Long running task begins')
    # sleep 5 seconds
    time.sleep(5)
    print(f'Long running task finished with result {x*y}')
    return x * y
