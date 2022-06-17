import uuid

from django.db import models
from django.utils import timezone

from .managers import SoftDeletionManager


class TimeAndUUIDStampedBaseModel(models.Model):
    """
    Base model class that contains special fields other model classes will subclass from

    Fields:
        created_at (DateTime): Time at which the object was created
        updated_at (Datetime): Time at which the object was updated
        uuid (String): UUID representing ID of each model
    """

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SoftDeleteBaseModel(models.Model):
    """
    Base model class that implements soft deletion for other models that will subclass from

    Fields:
        deleted_at (DateTime): Time at which action to delete an object was taken
    """

    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, hard=False):
        if hard:
            super(SoftDeleteBaseModel, self).delete()
        else:
            self.deleted_at = timezone.now()
            self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
