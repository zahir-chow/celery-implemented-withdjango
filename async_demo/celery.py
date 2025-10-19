import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_demo.settings')

app = Celery('async_demo')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    return f'Request: {self.request!r}'


