from django.db.models import IntegerChoices, TextChoices


class UserPrefix(TextChoices):
    MRS = "Mrs."
    MR = "Mr."
    MS = "Ms."
    MISS = "Miss."
    MX = "Mx."
    DR = "Dr."
    PROF = "Prof."
    REV = "Rev."
