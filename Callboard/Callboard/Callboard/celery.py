import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Callboard.settings')

app = Celery('Callboard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_mailing_10am': {
        'task': 'board.tasks.weekly_mailing',
        'schedule': crontab(hour=10, minute=0, day_of_week='monday'),
        'args': ()
    }
}