from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .managers import UserManager


# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=20,
        unique=True,
        null=True,
        blank=False,
        db_index=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("That username is not available"),
        },
    )

    email = models.EmailField(
        _("email address"),
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
        error_messages={
            "unique": _("That email is not available"),
        },
    )

    first_name = models.CharField(
        _("first name"), max_length=100, blank=False, null=False
    )

    last_name = models.CharField(
        _("last name"), max_length=100, blank=False, null=False
    )

    is_email_verified = models.BooleanField(_("is_email_verified"), default=False)

    email_verified_at = models.DateTimeField(
        _("email_verified_at"), blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        "username",
        "first_name",
        "last_name",
    )

    def get_absolute_url(self):
        return reverse("user-detail", args=[str(self.id)])

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.email

    objects = UserManager()

    @property
    def profile_url(self) -> str:
        hex_name = self.get_full_name().encode().hex()
        return f"https://avatars.dicebear.com/api/bottts/{hex_name}.svg/size=16"
