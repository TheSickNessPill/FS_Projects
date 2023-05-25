import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

# Реализовать рассылку уведомлений подписчикам после создания новости.
# Реализовать еженедельную рассылку с последними новостями (каждый понедельник в 8:00 утра)
app.conf.beat_schedule = {
    'send_news_every_md_18_00': {
        'task': 'news.tasks.send_last_week_news',
        'schedule': crontab(day_of_week="monday", hour=8),
        'args': ()
    },
}