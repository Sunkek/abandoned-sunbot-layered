#!/bin/sh
python manage.py makemigrations api
python manage.py migrate api
exec "$@"