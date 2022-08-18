import string

import factory.fuzzy
import faker
from django.utils import timezone

from accounts.enums import UserPrefix
from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.LazyAttribute(lambda obj: "%s@example.com" % obj.username)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    prefix = factory.fuzzy.FuzzyChoice([x[0] for x in UserPrefix.choices])
    phone_number = factory.fuzzy.FuzzyText(prefix="+", length=12, chars=string.digits)
    job_title = factory.Faker("job")
    company = factory.Faker("company")
    website = factory.LazyAttribute(lambda obj: "%s.faker.org" % obj.username)
    blog = factory.LazyAttribute(lambda obj: "%s.blog.faker.org" % obj.username)
    country = factory.Faker("country_code")
    postal_code = factory.Faker("postalcode")
    is_email_verified = factory.Faker("pybool")
    email_verified_at = factory.Faker(
        "date_time", tzinfo=timezone.get_current_timezone()
    )
    password = factory.PostGenerationMethodCall(
        "set_password",
        faker.Faker().password(
            length=20,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        ),
    )
