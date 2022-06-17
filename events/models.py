from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from timezone_field import TimeZoneField

from commons.models import TimeAndUUIDStampedBaseModel

from .enums import Category, LocationType, TimingType, Type


class Event(TimeAndUUIDStampedBaseModel):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        db_index=True,
    )
    title = models.CharField(
        _("title"),
        max_length=100,
        null=False,
        blank=False,
    )
    summary = models.CharField(_("description"), max_length=150)
    description = models.CharField(_("description"), max_length=2500)
    url = models.CharField(_("url"), max_length=500)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title}"


class Category(models.Model):
    event = models.ManyToManyField(Event)
    category = models.CharField(
        _("category"), choices=Category.choices, null=True, blank=True, max_length=1500
    )


class Type(models.Model):
    event = models.ManyToManyField(Event)
    etype = models.CharField(
        _("type"), choices=Type.choices, null=True, blank=True, max_length=100
    )


class Location(models.Model):
    event = models.ManyToManyField(Event)
    loc_type = models.CharField(
        _("location_type"),
        choices=LocationType.choices,
        null=False,
        blank=False,
        default=LocationType.VENUE,
        max_length=100,
    )
    location = models.CharField(_("location"), null=True, blank=True, max_length=1500)


class Image(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.FileField(upload_to="event_images", blank=True, null=True)


class Video(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    video = models.FileField(upload_to="event_videos", blank=True, null=True)


class Time(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timing_type = models.CharField(
        _("timing_type"),
        choices=TimingType.choices,
        null=False,
        blank=False,
        default=TimingType.SINGLE,
        max_length=100,
    )
    tz = TimeZoneField(default="Africa/Lagos", choices_display="WITH_GMT_OFFSET")
    start_date = models.DateTimeField(_("start date"))
    end_date = models.DateTimeField(_("end date"))
    start_time = models.TimeField(
        _("start_time"),
    )
    end_time = models.TimeField(_("end_time"))


class Ticket(TimeAndUUIDStampedBaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(_("name"), null=False, blank=False, max_length=100)
    description = models.CharField(
        _("quantity_description"), null=True, blank=True, max_length=2500
    )
    quantity = models.PositiveIntegerField(_("quantity"), null=True, blank=True)
    price = models.PositiveIntegerField(_("price"), null=True, blank=True)
    tickets_per_order = models.PositiveIntegerField(
        _("tickets_per_order"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
