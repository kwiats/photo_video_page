#!/bin/bash
python3 manage.py migrate
python3 manage.py collectstatic --noinput
celery -A core worker --loglevel=info &
celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &
ln -s staticfiles core/static
python3 manage.py runserver 0.0.0.0:8000