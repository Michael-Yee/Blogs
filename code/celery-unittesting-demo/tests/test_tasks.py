from celery.exceptions import Retry
from pytest import raises
from unittest.mock import patch
from proj.tasks import add, square


class TestAddTask(object):


    def test_add_success(self):
        add_result = add(x=1, y=2)
        assert add_result == 3


    @patch('proj.tasks.mul')
    @patch('proj.tasks.square.retry')
    def test_square_retry(self, square_retry, mul):
        # Set a side effect on the patched methods, so that they raise the errors we want.
        square_retry.side_effect = Retry()
        mul.side_effect = Exception()

        with raises(Retry):
            square(3)
            mul.assert_called_with(3)
