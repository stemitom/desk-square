from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Events(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    title = models.CharField(_("title"), max_length=500)
    description = models.CharField(_("description"), max_length=5000)
    place = models.CharField(_("place"), max_length=500)
    start_date = models.DateTimeField(_("start date"))
    end_date = models.DateTimeField(_("end date"))
    url = models.CharField(_("url"), max_length=500)

    class Meta:
        ordering = ("start_date",)

    def __str__(self):
        return f"{self.title}"


class Category(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=False)
