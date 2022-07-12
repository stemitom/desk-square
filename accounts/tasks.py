from datetime import timedelta

from celery import shared_task
from celery.schedules import crontab
from django.utils import timezone

from config.celery import app

from .models import User
from .utils import send_activation_mail, send_passsword_reset_mail


@shared_task
def delete_unverified_accounts():
    grace_period = timezone.now() - timedelta(hours=24)
    User.objects.filter(date_joined__lt=grace_period, is_email_verified=False).delete()


@app.task
def send_async_account_activation_mail(user_pk, request):
    send_activation_mail(user_pk, request)


@app.task
def send_async_password_reset_mail(email, request):
    send_passsword_reset_mail(email, request)


CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "config.tasks.sample_task",
        "schedule": crontab(hour="*/6"),
    },
}
