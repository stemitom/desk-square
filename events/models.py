import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from timezone_field import TimeZoneField

from commons.models import TimeAndUUIDStampedBaseModel

from .enums import Category, EType, LocationType, TimingType


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
        db_index=True,
    )
    summary = models.CharField(_("summary"), max_length=150)
    description = models.CharField(
        _("description"), null=True, blank=True, max_length=2500
    )
    url = models.URLField(_("url"), null=True, blank=True, max_length=500)

    category = models.CharField(
        _("category"), choices=Category.choices, null=True, blank=True, max_length=1500
    )
    event_type = models.CharField(
        _("type"), choices=EType.choices, null=True, blank=True, max_length=100
    )

    loc_type = models.CharField(
        _("location_type"),
        choices=LocationType.choices,
        null=False,
        blank=False,
        default=LocationType.VENUE,
        max_length=100,
    )
    location = models.CharField(_("location"), null=True, blank=True, max_length=1500)

    timing_type = models.CharField(
        _("timing_type"),
        choices=TimingType.choices,
        null=False,
        blank=False,
        default=TimingType.SINGLE,
        max_length=100,
    )
    tz = TimeZoneField(default="Africa/Lagos", choices_display="WITH_GMT_OFFSET")
    start_date = models.DateField(_("start date"), default=datetime.date.today)
    start_time = models.TimeField(_("start_time"), null=True, blank=True)
    end_date = models.DateField(_("end date"), default=datetime.date.today)
    end_time = models.TimeField(_("end_time"), null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title}"


class Tag(models.Model):
    event = models.ManyToManyField(Event, related_name="tags")
    tag_regex = RegexValidator(
        regex="^[A-Za-z0-9_]+$",
        message="Tags can only contain letters, numbers and underscores",
    )
    name = models.CharField(
        _("tag"), validators=[tag_regex], null=True, blank=True, max_length=50
    )

    def __str__(self) -> str:
        return self.name


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


class Image(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.FileField(upload_to="event_images", blank=True, null=True)


class Video(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    video = models.FileField(upload_to="event_videos", blank=True, null=True)
