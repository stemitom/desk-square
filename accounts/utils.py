from logging import getLogger

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .tokens import account_activation_token, account_password_reset_token

logger = getLogger(__name__)

User = get_user_model()


def create_account_activation_url(uid, token, request):
    endpoint = reverse("accounts:activate", kwargs={"uid": uid, "token": token})
    url = request.build_absolute_uri(endpoint)
    return url


def send_activation_mail(user_pk: int, request):
    """Utility function that sends account activation email"""
    logger.info(f"Sending activation email to: {user_pk}")

    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        logger.warning(f"Error: User does not exist -> {user_pk}")
        pass

    uid = urlsafe_base64_encode(force_bytes(user_pk))
    token = account_activation_token.make_token(user)
    url = create_account_activation_url(uid, token, request)

    subject = "[Desk Square] Activate Your Account"
    html_content = render_to_string(
        "accounts/emails/activation.htm",
        {"first_name": user.first_name, "last_name": user.last_name, "url": url},
    )

    mail = EmailMultiAlternatives(subject, to=[user.email])
    mail.attach_alternative(html_content, "text/html")
    mail.send()

    logger.info(f"Activation email successfully sent to -> {user.username}")


def send_passsword_reset_mail(user_pk: int, request):
    """Utility function that sends password reset email"""
    logger.info(f"Sending Password Reset email to: {user_pk}")

    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        logger.warning(f"Error: User does not exist -> {user_pk}")
        pass

    uid = urlsafe_base64_encode(force_bytes(user_pk))
    token = account_password_reset_token.make_token(user)
    url = create_account_activation_url(uid, token, request)

    subject = "[Desk Square] Reset Your Password"
    html_content = render_to_string(
        "accounts/emails/password_reset.htm",
        {"first_name": user.first_name, "last_name": user.last_name, "url": url},
    )

    mail = EmailMultiAlternatives(subject, to=[user.email])
    mail.attach_alternative(html_content, "text/html")
    mail.send()

    logger.info(f"Password reset email successfully sent to -> {user.username}")


def verify_uid_and_token(uid: str, token: str, type: str):
    """Utility function that verifies uid and token in password reset and email confirmations."""
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if type == "activation":
        if user is not None and account_activation_token.check_token(user, token):
            return (user, True)
    elif type == "reset":
        if user is not None and account_password_reset_token.check_token(user, token):
            return (user, True)

    return (user, False)
