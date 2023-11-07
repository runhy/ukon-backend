#! /bin/sh


echo "run db init"
python /app/manage.py db init

echo "run db migrate"
python /app/manage.py db migrate

echo "run db upgrade"
python /app/manage.py db upgrade

echo "run initialize"
python manage.py init data

echo "db done"

