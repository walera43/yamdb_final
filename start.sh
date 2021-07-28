#!/bin/bash
python manage.py makemigrations reviews --noinput
python manage.py makemigrations titles --noinput
python manage.py makemigrations users --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000