#!/bin/sh
apt-get update && apt-get install -y netcat
echo "Waiting for API..."
  while ! nc -z $API_HOST $API_PORT; do
    sleep 0.1
    done
  echo "API started"

exec "$@"