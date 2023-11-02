#! /bin/sh

source .env
# Wait for PostgreSQL
until nc -z -v -w30 $POSTGRES_HOST $POSTGRES_PORT
do
  echo 'Waiting for PostgreSQL...'
  sleep 1
done
echo "PostgreSQL is up and running"
