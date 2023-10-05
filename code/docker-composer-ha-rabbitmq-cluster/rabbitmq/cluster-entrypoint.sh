#!/bin/bash

set -e

echo "Running entrypoint script for RabbitMQ clustering"
echo ""
echo ""
echo "Starting RabbitMQ Server... "

if [ -z "$CLUSTER_WITH" ]; then
  echo "Starting standalone mode"
  /usr/local/bin/docker-entrypoint.sh rabbitmq-server
  rabbitmqctl stop_app
  sleep 10  
  rabbitmqctl reset
  sleep 10  
  rabbitmqctl stop
  sleep 10
  rabbimq-server
  
else
  echo "Starting clustering mode"
  /usr/local/bin/docker-entrypoint.sh rabbitmq-server -detached
  sleep 10
  rabbitmqctl stop_app
  sleep 10  
  rabbitmqctl reset
  sleep 10  

  if [ -z "$RAM_NODE" ]; then
      rabbitmqctl join_cluster rabbit@$CLUSTER_WITH
      sleep 10      
    else
      rabbitmqctl join_cluster --ram rabbit@$CLUSTER_WITH
      sleep 10      
  fi
  
  rabbitmqctl stop
  sleep 10
  rabbitmq-server
fi
