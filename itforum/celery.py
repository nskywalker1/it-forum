import os
from celery import Celery

from itforum import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itforum.settings')

app = Celery('itforum')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
