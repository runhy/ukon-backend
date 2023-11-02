#! /bin/sh

source .env
echo "run db init"
python manage.py db init

echo "run db migrate"
python manage.py db migrate

echo "run db upgrade"
python manage.py db upgrade

#echo "run initialize"
#python manage.py initialize

echo "db done"

