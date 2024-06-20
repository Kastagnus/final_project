from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# სელერის აპლიკაციასთან დაკავშირების კონფიგურაცია, რომელც უყურებს shared_task-ებს
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'royaltravel.settings')

app = Celery('royaltravel')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
