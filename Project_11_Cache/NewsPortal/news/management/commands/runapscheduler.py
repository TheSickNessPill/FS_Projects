import logging
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import (
    mail_managers,
    send_mail
)
from news.models import (
    Post,
    Category,
    Subscription
)
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def my_job():
    categoryes = Category.objects.filter()

    previous_week_datetime = datetime.datetime.now() - datetime.timedelta(days=7, minutes=1)

    for category in categoryes:
        category_posts = Post.objects.filter(category)
        category_posts = filter(
            lambda post:
                post.post_create_datetime > previous_week_datetime,
            category_posts
        )
        category_posts = "\n".join(
            ["{} - {}".format(post.post_title, post.get_absolute_url()) for post in category_posts]
        )
        category_subs = Subscription.objects.filter(category_id=category)
        category_subs = [User.objects.filter(id=sub.user_id)[0].email for sub in category_subs]

        send_mail(
            subject='Список Новостей',
            message=category_posts,
            from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
            recipient_list=category_subs,
        )


# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week=4,
                hour="18",
                minute="00",
            ),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
