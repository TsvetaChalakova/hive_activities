from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hive_activities.settings')

app = Celery('hive_activities')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in all installed apps. Sometimes things have simple names.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
