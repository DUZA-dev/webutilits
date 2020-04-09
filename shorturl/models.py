from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from core.models import Hint


class Protocol(models.Model):
    # Хранит в себе протоколы, на которые ссылаются url адресса
    protocol = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.protocol


class Url(models.Model):
    # Хранит в себе значения URL-адрессов, соотносящиеся с сокращенным адресомы
    url = models.TextField(null=False, blank=False)
    url_short = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True
    )

    pub_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    creator_ip = models.CharField(max_length=15, null=False, blank=False)

    hints = GenericRelation(Hint, related_name="urls")

    protocol = models.ForeignKey(
        Protocol,
        related_name="urls",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
