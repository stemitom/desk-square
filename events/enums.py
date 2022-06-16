from django.db.models import TextChoices


class Type(TextChoices):
    APPEARANCE = "Appearance & Signing"
    ATTRACTION = "Attraction"
    CAMP = "Camp, Trip and Retreat"
    CONCERT = "Concert Performance"
    CONFERENCE = "Conference"
    CONVENTION = "Convention"
    DINNER = "Dinner or Gala"
    FESTIVAL = "Festival or Fair"
    GAME = "Game or Competition"
    MEETING = "Meeting or Network Events"
    OTHER = "Other"
    PARTY = "Party or Social Gathering"
    RACE = "Race or Endurance Event"
    RALLY = "Rally"
    SCREENING = "Screening"
    SEMINAR = "Seminar"
    TOUR = "Tour"
    TRADESHOW = "Tradeshow or Expo"
    TYPE = "Type"


class Category(TextChoices):
    AUTO = "Auto, Boat & Air"
    BUSINESS = "Business and Professional"
    CHARITY = "Charity & Causes"
    COMMUNITY = "Community"
    FAMILY = "Family & Education"
    FASHION = "Fashion & Beauty"
    FILM = "Film & Entertainment"
    FOOD = "Food & Drink"
    CATEGORY = "Category"


class LocationType(TextChoices):
    VENUE = "Venue"
    ONLINE = "Online"
    INPERSON = "In Person"


class TimingType(TextChoices):
    SINGLE = "Single Event"
    RECURRING = "Recurring Event"
