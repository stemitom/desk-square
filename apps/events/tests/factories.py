import factory.fuzzy
from timezone_field import TimeZoneField

from apps.accounts.tests.factories import UserFactory
from apps.events.enums import Category, EventType, LocationType, MediaType, TimingType
from apps.events.models import Attendee, Event, Location, Tag, TicketOrder


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    creator = factory.SubFactory(UserFactory)
    title = factory.fuzzy.FuzzyText()
    summary = factory.Faker("paragraph", nb_sentences=3)
    url = factory.LazyAttribute(lambda obj: "%s.faker.org" % obj.title)
    category = factory.fuzzy.FuzzyChoice(choice[0] for choice in  Category.choices)
    event_type = factory.fuzzy.FuzzyChoice(choice[0] for choice in EventType.choices)
    timing_type = factory.fuzzy.FuzzyChoice(choice[0] for choice in TimingType.choices)
    tz = factory.fuzzy.FuzzyChoice(choice for choice in TimeZoneField.default_pytz_tzs)

class UserOrganizingMultipleEventsFactory(UserFactory):
    @factory.post_generation
    def events(self, create, num_of_events, **kwargs):
        if not create: return
        if num_of_events is None: num_of_events = 1
        for _ in range(num_of_events):
            EventFactory(creator=self)


class AttendeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attendee

    user = factory.SubFactory(UserFactory)
    event = factory.SubFactory(EventFactory)


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    event = factory.SubFactory(EventFactory)
    location_type = factory.fuzzy.FuzzyChoice(choice[0] for choice in LocationType.choices)
    location = factory.Faker("address")


class TagFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()

    @factory.post_generation
    def events(self, create, extracted, **kwargs):
         if not create: return
         if extracted:
             for event in extracted:
                 self.events.add(event)


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.fuzzy.FuzzyText()
    event = factory.SubFactory(EventFactory)
    description = factory.Faker("paragraph", nb_sentences=3)
    quantity_available = factory.fuzzy.FuzzyInteger(100)
    unit_price = factory.fuzzy.FuzzyDecimal(5.00)


class TicketOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TicketOrder

    user = factory.SubFactory(AttendeeFactory)
    tickets_purchased = factory.SubFactory(TicketFactory)