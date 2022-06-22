import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from commons.models import TimeAndUUIDStampedBaseModel

from .enums import Category, EventType, LocationType, TimingType, MediaType


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
    description = models.TextField(
        _("description"), null=True, blank=True, max_length=2500
    )
    url = models.URLField(_("url"), null=True, blank=True, max_length=500)

    category = models.CharField(
        _("category"), choices=Category.choices, null=True, blank=True, max_length=1500
    )
    event_type = models.CharField(
        _("type"), choices=EventType.choices, null=True, blank=True, max_length=100
    )

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

    @property
    def is_recurrent(self):
        return self.timing_type == TimingType.RECURRING


class Location(models.Model):
    event = models.OneToOneField(
        Event, on_delete=models.CASCADE, related_name="location"
    )
    location_type = models.CharField(
        _("location_type"),
        choices=LocationType.choices,
        null=False,
        blank=False,
        default=LocationType.VENUE,
        max_length=100,
    )
    location = models.CharField(_("location"), null=True, blank=True, max_length=1500)
    conference_uri = models.URLField(_("conference_uri"), null=True, blank=True)
    lat = models.DecimalField(
        _("lat"), max_digits=22, decimal_places=16, null=True, blank=True
    )
    long = models.DecimalField(
        _("long"), max_digits=22, decimal_places=16, null=True, blank=True
    )
    state = models.CharField(_("state"), null=True, blank=True, max_length=20)
    country = CountryField(_("country"), null=True, blank=True)


class Tag(models.Model):
    event = models.ManyToManyField(Event, related_name="tags")
    tag_regex = RegexValidator(
        regex="^[A-Za-z0-9_]+$",
        message="Tags can only contain letters, numbers and underscores",
    )
    name = models.CharField(
        _("tag"),
        validators=[tag_regex],
        null=True,
        blank=True,
        max_length=50,
        db_index=True,
    )

    def __str__(self) -> str:
        return self.name


class Ticket(TimeAndUUIDStampedBaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    name = models.CharField(_("name"), null=False, blank=False, max_length=100)
    description = models.CharField(
        _("quantity_description"), null=True, blank=True, max_length=2500
    )
    quantity = models.PositiveIntegerField(_("quantity"), null=True, blank=True)
    price = models.DecimalField(
        _("price"), max_digits=22, decimal_places=5, null=True, blank=True
    )
    tickets_per_order = models.PositiveIntegerField(
        _("tickets_per_order"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )


class Media(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    file = models.FileField(upload_to="event_uploads", null=True, blank=True)
    type = models.CharField(
        _("type"), choices=MediaType.choices, null=True, blank=True, max_length=10
    )
