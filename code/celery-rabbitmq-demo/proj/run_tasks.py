from  proj.tasks import add, mul
from proj.celeryconfig import A_QUEUE, M_QUEUE
import time


if __name__ == '__main__':
    add_result = add.apply_async((2, 2), queue=A_QUEUE)
    # sleep 1 seconds to ensure the task has been finished
    time.sleep(1)
    # now the task should be finished and ready method will return True
    print(f'add task finished? {add_result.ready()}')
    print(f'add task result: {add_result.result}')

    mul_result = mul.delay(3, 3)
    # at this time, our task is not finished, so it will return False
    print(f'mul task finished? {mul_result.ready()}')
    print(f'mul task result: {mul_result.result}')
    # sleep 10 seconds to ensure the task has been finished
    time.sleep(10)
    # now the task should be finished and ready method will return True
    print(f'mul task finished? {mul_result.ready()}')
    print(f'mul task result: {mul_result.result}')
    