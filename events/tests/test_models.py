import datetime

from django.db.utils import IntegrityError
from django.test import TestCase

from accounts.models import User
from events.models import Event, Tag


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
            loc_type="Online",
            location="https://meet.google.com",
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
        print(event.tz)

    def test_event_creation(self) -> None:
        testevent = Event.objects.get(title="Django Meetup - Lagos Branch")
        self.assertTrue(isinstance(testevent, Event))
        self.assertEqual(str(testevent), testevent.title)
