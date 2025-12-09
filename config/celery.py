import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Настройка периодических задач
app.conf.beat_schedule = {
    'block-inactive-users-every-day': {
        'task': 'users.tasks.block_inactive_users', # Путь к задаче
        'schedule': crontab(hour=0, minute=0), # Запуск каждый день в 00:00
    },
}
