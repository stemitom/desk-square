import datetime
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from commons.models import TimeAndUUIDStampedBaseModel

from .enums import Category, EventType, LocationType, MediaType, TimingType


class Event(TimeAndUUIDStampedBaseModel):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        db_index=True,
        related_name="events",
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

    @property
    def ticket_details(self):
        return self.ticket.all()


class Attendee(TimeAndUUIDStampedBaseModel):
    name = models.CharField(_("name"), null=True, blank=True, max_length=100)
    email = models.EmailField(
        _("email"), null=True, blank=True, max_length=100, db_index=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="attendees",
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendees")
    guest = models.BooleanField(_("guest"), default=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["email", "event"], name="email_register_event_once"
            ),
        ]
        ordering = ("-created_at",)

    def clean(self) -> None:
        if not self.user:
            if not (self.name and self.email):
                raise ValidationError(
                    {
                        "attendee": "name and email should be supplied if registering for an event as a guest"
                    }
                )
            self.guest = True
        return super(Attendee, self).clean()

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super(Attendee, self).save(*args, **kwargs)


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
        unique=True,
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
    quantity_available = models.PositiveIntegerField(
        _("quantity"), null=True, blank=True
    )
    unit_price = models.DecimalField(
        _("price"), max_digits=22, decimal_places=5, null=True, blank=True
    )
    max_tickets_per_order = models.PositiveIntegerField(
        _("tickets_per_order"),
        default=1,
        validators=[MinValueValidator(1)],
    )


class TicketOrder(TimeAndUUIDStampedBaseModel):
    user = models.ForeignKey(
        Attendee, on_delete=models.CASCADE, related_name="ticket_orders"
    )
    tickets_purchased = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="orders"
    )
    quantity = models.PositiveIntegerField(_("quantity"), default=1)
    order_id = models.UUIDField(
        _("order_id"), default=uuid.uuid4, db_index=True, unique=True
    )


class Media(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="medias")
    file = models.FileField(upload_to="event_uploads", null=True, blank=True)
    type = models.CharField(
        _("type"), choices=MediaType.choices, null=True, blank=True, max_length=10
    )
