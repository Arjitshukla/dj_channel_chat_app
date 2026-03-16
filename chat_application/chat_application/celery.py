import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_application.settings")

app = Celery("chat_application")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()