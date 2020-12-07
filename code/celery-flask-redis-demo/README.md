# Getting Started

NOTE: This repo is a work in progress


## Gmail:

Set less secure app access = ON

## Environment settings

set MAIL_USERNAME=MAIL_USERNAME@gmail.com

set MAIL_PASSWORD=MAIL_PASSWORD

## Requirements

```
pip install -r requirements.txt
```

## Redis

```
version: "3.7"

services:

  redis:
    image: redis:latest
    ports:
      - 6379:6379
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - redis-data:/data

  redis-commander:
    image: rediscommander/redis-commander:latest
    environment:
      - REDIS_HOSTS=local:redis:6379
      - HTTP_USER=root
      - HTTP_PASSWORD=qwerty
    ports:
      - 8081:8081
    depends_on:
      - redis
    
volumes:
  redis-data:
```

```
docker-compose up -d
docker-compose down -v
```

## Celery

```
celery -A app.celery worker
```

## Application

```
python app.py
```