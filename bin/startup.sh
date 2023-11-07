#! /bin/sh

source .env

#/bin/bash ./docker/wait-for-services.sh
/bin/bash /app/bin/prepare-db.sh

export $(cat .env | xargs) && /bin/bash /app/bin/docker-entrypoint server
#export $(cat .env | xargs) && /usr/local/bin/gunicorn -c settings/gunicorn.py "lib.create_app:create_app()"
