from django.db.models import TextChoices


class Type(TextChoices):
    APS = "Appearance & Signing"
    ATR = "Attraction"
    CTR = "Camp, Trip and Retreat"
    CONP = "Concert Performance"
    CONF = "Conference"
    CONV = "Convention"
    DING = "Dinner or Gala"
    FEST = "Festvial or Fair"
    GAMC = "Game or Competition"
    MENE = "Meeting or Network Events"
    OTH = "Other"
    PARS = "Party or Social Gathering"
    RAEV = "Race or Endurance Event"
    RALL = "Rally"
    SCRN = "Screening"
    SEMN = "Seminar"
    TOUR = "Tour"
    TREX = "Tradeshow or Expo"
    TYPE = "Type"


class Category(TextChoices):
    ABA = "Auto, Boat & Air"
    BP = "Business and Professional"
    CHC = "Charity & Causes"
    COM = "Community"
    FAM = "Family & Education"
    FAB = "Fashion & Beauty"
    FME = "Film & Entertainment"
    FOD = "Food & Drink"
    CAT = "Category"


class LocationType(TextChoices):
    VEN = "Venue"
    ONL = "Online"
    INP = "In Person"


class TimingType(TextChoices):
    SIN = "Single Event"
    REC = "Recurring Event"
