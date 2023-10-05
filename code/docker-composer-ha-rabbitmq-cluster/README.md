# Load balanced RabbitMQ Cluster - Docker Compose

This repo will create a 3 node RabbitMQ cluster using Docker Composer with HAProxy load balancer (round robin)

NOTE: Queue mirroring is not enabled (as suggestd by RabbitMQ docs: https://www.rabbitmq.com/ha.html), but we use the modern queue type Quorum Queues (https://www.rabbitmq.com/quorum-queues.html)

## Deploy

```bash
  docker compose up
```

NOTE: Ports 1936, 5672 and 15672 are required, otherwise TCP socket bind error will be shown.

## Validattion

### HAProxy statistics

n the browser, navigate to http://localhost:1936 with default credential admin:admin

### RabbitMQ cluster statue

In the command line,

```
docker exec -it docker-composer-ha-rabbitmq-cluster-rabbitmqmaster-1 bash -c "rabbitmqctl cluster_status"
```

### RabbitMQ management

In the browser, navigate to http://localhost:15672 with default credential admin:admin
