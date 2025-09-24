import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')

app = Celery('library_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'remind-overdue-books': {
        'task': 'library.tasks.remind_overdue_books',
        # 'schedule': crontab(hour=7, minute=0) # rum daily
        'schedule': crontab(minute="*/1") # testing
    }
}