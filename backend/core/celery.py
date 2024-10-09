import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('photo_app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_acks_late = True

app.autodiscover_tasks()
