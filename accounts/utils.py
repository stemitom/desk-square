from logging import getLogger

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.request import Request

from .tokens import account_activation_token, account_password_reset_token

logger = getLogger(__name__)

User = get_user_model()


def create_account_activation_url(uid, token, request):
    endpoint = reverse("accounts:activate", kwargs={"uid": uid, "token": token})
    url = request.build_absolute_uri(endpoint)
    return url


def send_mail(user_pk: int, request: Request, mail_type: str):
    var = {
        "activation": {
            "name": "activate",
            "token": account_activation_token,
            "template": "activation.htm",
            "subject": "Activate Your Account"
        },
        "reset": {
            "name": "reset",
            "token": account_password_reset_token,
            "template": "password_reset.htm",
            "subject": "Reset Your Password"
        },
    }

    logger.info(f"Sending {mail_type}.capitalize() email to: user {user_pk}")
    token = var[mail_type]["token"]
    template = var[mail_type]["template"]
    subject = var[mail_type]["subject"]

    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        logger.warning(f"Error: User does not exist -> {user_pk}")
        pass

    uid = urlsafe_base64_encode(force_bytes(user_pk))
    token = token.make_token(user)
    url = create_account_activation_url(uid, token, request)

    subject = f"[Desk Square] {subject}"
    html_content = render_to_string(
        f"accounts/emails/{template}",
        {"first_name": user.first_name, "last_name": user.last_name, "url": url},
    )

    mail = EmailMultiAlternatives(subject, to=[user.email])
    mail.attach_alternative(html_content, "text/html")
    mail.send()

    logger.info(f"{mail_type}.capitalize() email successfully sent to -> {user.username}")


def send_activation_mail(user_pk: int, request: Request):
    """Utility function that sends account activation email"""
    send_mail(user_pk, request, mail_type="activation")


def send_password_reset_mail(user_pk: int, request: Request):
    """Utility function that sends password reset email"""
    send_mail(user_pk, request, mail_type="reset")


def verify_uid_and_token(uid: str, token: str, token_type: str):
    """Utility function that verifies uid and token in password reset and email confirmations."""
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if token_type == "activation":
        if user is not None and account_activation_token.check_token(user, token):
            return user, True
    elif token_type == "reset":
        if user is not None and account_password_reset_token.check_token(user, token):
            return user, True

    return user, False
