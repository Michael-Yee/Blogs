---
title: Unit testing Celery Tasks
author: Michael Yee
published: True
---


# Overview

In this blog, I will introduce how I write unit tests for Celery tasks using the pytest framework.


## Structure

We will start off from where were left off in my other blog: Celery using RabbitMQ.  

In the parent folder, create a folder named tests.

    +--parent
    |  +--tests
    |  +--proj
    |  |  +--__init__.py
    |  |  +--celery.py
    |  |  +--celeryconfig.py
    |  |  +--tasks.py
    |  |  +--run_tasks.py

## tasks.py:

We have modified our original tasks.py to add in a new function called square and removed all the print statements.

```python
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

```

## test_tasks.py

Create a file named test_tasks.py with the following code in the tests folder.  In test_tasks.py, the mock module is used to patch methods and create desired side effects. 

```python
from celery.exceptions import Retry
from pytest import raises
from unittest.mock import patch
from proj.tasks import add, square


class TestAddTask(object):


    def test_add_success(self):
        add_result = add(x=1, y=2)
        assert add_result == 3


    @patch('proj.tasks.mul') # < patching mul in module proj.tasks
    @patch('proj.tasks.square.retry')
    def test_square_retry(self, square_retry, mul):
        # Set a side effect on the patched methods, so that they raise the errors we want
        square_retry.side_effect = Retry()
        mul.side_effect = Exception()

        with raises(Retry):
            square(3)
            mul.assert_called_with(3)


```

NOTE: Type "python -m pytest" in parent folder to run the above tests.

## Eager mode

The eager mode enabled by the task_always_eager setting is by definition not suitable for unit tests.

When testing with eager mode you are only testing an emulation of what happens in a worker, and there are many discrepancies between the emulation and what happens in reality.

A sample of unit testing Celery task with eager mode would be as follows:

```python
conftest.py
from myproject.myapp import celeryapp


@pytest.fixture(scope='module')
def celery_app(request):
    celeryapp.conf.update(task_always_eager=True)
    return celeryapp


test_tasks.py
def test_some_task(celery_app):
    ...
```

In the above code, the fixture starts a Celery worker instance that you can use for integration tests. The worker will be started in a separate thread and will be shutdown as soon as the test returns. To read more about pytest fixture -> https://docs.pytest.org/en/latest/fixture.html#fixture

NOTE: If you wish to override some setting in one test cases only - you can use the pytest.mark


# Conclusion

To test Celery task behavior in unit tests the preferred method is mocking.

