from config.celery import app

from datetime import timedelta
from django.utils import timezone

from .models import User
from .utils import send_activation_mail, send_passsword_reset_mail


# from huey import crontab
# from huey.contrib.djhuey import db_periodic_task, db_task

# @db_periodic_task(crontab(hour="*/3"))
# def delete_unverified_accounts():
#     grace_period = timezone.now() - timedelta(hours=24)
#     unverified_users = User.objects.filter(
#         date_joined__lt=grace_period, is_email_verified=False
#     ).delete()


@app.task
def send_async_account_activation_mail(user_pk, request):
    send_activation_mail(user_pk, request)


@app.task
def send_async_password_reset_mail(email, request):
    send_passsword_reset_mail(email, request)
