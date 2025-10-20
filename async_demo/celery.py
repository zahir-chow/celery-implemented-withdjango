import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_demo.settings')

app = Celery('async_demo')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Additional Celery configuration for better Redis handling
app.conf.update(
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=10,
    task_soft_time_limit=60,
    task_time_limit=120,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_disable_rate_limits=False,
)

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    return f'Request: {self.request!r}'


