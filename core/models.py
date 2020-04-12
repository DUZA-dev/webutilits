from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class UserCounter(models.Model):
    ip = models.CharField(max_length=15, null=False, blank=False)

    date = models.DateTimeField(auto_now=True, null=False, blank=False)

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)

    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class Download(UserCounter):
    pass


class Hint(UserCounter):
    pass
