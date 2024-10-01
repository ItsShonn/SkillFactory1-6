import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from ...models import Category, User, UserToCategory, Post

logger = logging.getLogger(__name__)

from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils import timezone
import os


def send_mail_to_subscriber():

    for cat in Category.objects.all():
        enddate = datetime.now(tz=timezone.get_current_timezone())
        startdate = enddate - timedelta(days=7)
        posts = Post.objects.filter(categories=cat).filter(date__range=[startdate, enddate])
        if posts:
            subscribers = []
            message = f'Вышедшие записи:\n'
            for post in posts:
                message += f'127.0.0.1:8000/news/{post.id}\n'
            connections = UserToCategory.objects.all()
            for connection in connections.filter(category=cat):
                subscribers.append(User.objects.get(id=connection.user.id).email)
            send_mail(
                subject=f'{cat}: Еженедельная рассылка на подписанную вами категорию!',
                message=message,
                from_email=str(os.getenv('EMAIL')) + '@yandex.ru',
                recipient_list=subscribers
            )
        else:
            pass


def delete_old_job_executions(max_age=604_800):

    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_mail_to_subscriber,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),

            id="send_mail_to_subscriber",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_mail_to_subscriber'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),

            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")