import uuid

from django.db import models, DEFAULT_DB_ALIAS
from django.utils import timezone
from simple_history.models import HistoricalRecords


class DeletableQueryManager(models.Manager):
    def get_queryset(self):
        return super(DeletableQueryManager, self).get_queryset().filter(is_deleted__in=[False])

    def get_deleted(self):
        return super(DeletableQueryManager, self).get_queryset().filter(is_deleted__in=[True])


class DeletableModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = DeletableQueryManager()
    default_manager = models.Manager()

    def delete(self, using=DEFAULT_DB_ALIAS, keep_parents=False):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class IPAddressHistoricalModel(models.Model):
    ip_address = models.GenericIPAddressField('IP address', null=True)

    class Meta:
        abstract = True


class CommonModel(DeletableModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    create_date = models.DateTimeField(editable=False, default=timezone.now)
    update_date = models.DateTimeField(editable=False, auto_now=True)

    history = HistoricalRecords(
        inherit=True,
        bases=[IPAddressHistoricalModel, ]
    )

    class Meta:
        ordering = ["-update_date"]
        abstract = True
