import datetime

from django.test import TestCase

from accounts.models import User
from events.models import Event, Location, Tag


class TestModels(TestCase):
    def setUp(self) -> None:
        creator = User.objects.create(
            email="testuser@gmail.com",
            username="testuser",
            first_name="Test",
            last_name="User",
        )
        event = Event.objects.create(
            creator=creator,
            title="Django Meetup - Lagos Branch",
            summary="Django DRF",
            description="Let's discuss the detailed aspects of DRF and its wonders",
            url="https://www.django-rest-framework.org/api-guide/serializers/#modelserializer",
            category="Technology",
            event_type="Conference",
            timing_type="Recurring",
            tz="Africa/Lagos",
            start_date=datetime.date(2022, 8, 8),
            start_time=datetime.time(10, 30, 00),
            end_date=datetime.date(2022, 8, 8),
            end_time=datetime.time(11, 00, 00),
        )

        tags = [
            Tag.objects.create(name="Django"),
            Tag.objects.create(name="API"),
        ]
        event.tags.add(*tags)

        Location.objects.create(
            event=event,
            location_type="Venue",
            location="13th Redmond, CA",
            conference_uri="https://meet.google.com",
            lat="37.4267861",
            long="-122.0806032",
            state="California",
            country="USA",
        )

        event.tickets.create(
            name="Ticket #1",
            description="VIP Ticket",
            quantity_available="100",
            unit_price=5.50,
            max_tickets_per_order=1,
        )

    def test_event_creation(self) -> None:
        testevent = Event.objects.get(title="Django Meetup - Lagos Branch")
        self.assertTrue(isinstance(testevent, Event))
        self.assertEqual(str(testevent), testevent.title)

    def test_event_recurrent(self) -> None:
        testevent = Event.objects.get(title="Django Meetup - Lagos Branch")
        print(testevent.is_recurrent)
        self.assertIs(testevent.is_recurrent, True)
