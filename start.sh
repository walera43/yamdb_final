#!/bin/bash
python manage.py makemigrations reviews
python manage.py makemigrations titles
python manage.py makemigrations users
python manage.py migrate
python manage.py collectstatic
gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000