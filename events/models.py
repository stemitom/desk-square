from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Events(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(_("title"), max_length=500)
    descriptiion = models.CharField(_("description"), max_length=5000)
    place = models.CharField(
        _("place"),
        max_length=500,
    )
    start_date = models.DateTimeField(_("start date"))
    end_date = models.DateTimeField(_("end date"))
    url = models.CharField(_("url"), max_length=500)

    class Meta:
        ordering = ("start_date",)

    def __str__(self):
        return f"{self.title}"


class Tickets(models.Model):
    pass
