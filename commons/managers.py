from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


class SoftDeletionQuerySet(QuerySet):
    def delete(self, hard=False):
        if hard:
            return super(SoftDeletionQuerySet, self).delete()
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def get_queryset(self):
        return SoftDeletionQuerySet(self.model).filter(deleted_at__isnull=True)
