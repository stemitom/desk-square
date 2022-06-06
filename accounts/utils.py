from logging import getLogger

from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User
from .tokens import account_activation_token, account_password_reset_token

logger = getLogger(__name__)


def create_account_activation_url(uid, token, request):
    endpoint = reverse("accounts:activate")
    protocol = "https" if request.is_secure() else "http"
    host = request.get_host()

    return f"{protocol}://{host}{endpoint}?uid={uid}&token={token}"


def send_verification_email(
    user, request, sender, subject="Verify your email", message=""
):
    uid = urlsafe_base64_decode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    message += create_account_activation_url(uid, token, request)
    send_mail(
        "Subject here",
        "Here is the message.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )
