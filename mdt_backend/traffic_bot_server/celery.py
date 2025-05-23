import os
from celery import Celery

os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_bot_server.settings')

celery = Celery('traffic_bot_server')

# Load task modules from all registered Django app configs.
celery.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
celery.autodiscover_tasks()
