from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .enums import Type, Category, LocationType, TimingType
from timezone_field import TimeZoneField


class Event(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    title = models.CharField(
        _("title"),
        max_length=100,
        null=False,
        blank=False,
    )
    summary = models.CharField(_("description", max_length=150))
    description = models.CharField(_("description"), max_length=5000)
    place = models.CharField(_("place"), max_length=500)
    url = models.CharField(_("url"), max_length=500)

    class Meta:
        ordering = ("start_date",)

    def __str__(self):
        return f"{self.title}"


class Category(models.Model):
    event = models.ManyToManyField(Event)
    category = models.CharField(
        _("category"), choices=Category.choices, null=True, blank=True
    )


class Type(models.Model):
    event = models.ManyToManyField(Event)
    etype = models.CharField(_("type"), choices=Type.choices, null=True, blank=True)


class Location(models.Model):
    event = models.ManyToManyField(Event)
    loc_type = models.CharField(
        _("location_type"),
        choices=LocationType.choices,
        null=True,
        blank=True,
        default=LocationType.VEN,
    )
    location = models.CharField(_("location"), null=True, blank=True)


class Time(models.Model):
    event = models.ForeignKey(Event)
    timing_type = models.CharField(
        _("timing_type"),
        choices=TimingType.choices,
        null=True,
        blank=True,
        default=TimingType.SINGLE,
    )
    timezone = models.CharField()
    tz = TimeZoneField(default="Africa/Lagos", choices_display="WITH_GMT_OFFSET")
    start_date = models.DateTimeField(_("start date"))
    end_date = models.DateTimeField(_("end date"))
    start_time = models.TimeField(_("start_time"))
    end_time = models.TimeField(_("end_time"))
