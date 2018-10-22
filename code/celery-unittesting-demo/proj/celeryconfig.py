# Iif you want to manually specify queue/exchange/binding key of Celery
#from kombu import Queue, Exchange


# Celery queues names
A_QUEUE = 'add_queue'
M_QUEUE = 'mul_queue'
S_QUEUE = 'square_queue'

# Broker settings
broker_url = 'amqp://172.17.0.2'
result_backend = 'rpc://'
imports = ['proj.tasks']
task_routes = {'proj.tasks.add': {'queue': A_QUEUE, 'routing_key': A_QUEUE}, 'proj.tasks.mul': {'queue': M_QUEUE, 'routing_key': M_QUEUE}, 'proj.tasks.square': {'queue': S_QUEUE, 'routing_key': S_QUEUE}}
