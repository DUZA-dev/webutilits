from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation

from core.models import Hint, Download


class File(models.Model):
    # Модель, кранящая сведения об опубликованном файле и путь до него
    file = models.FileField(upload_to='uploads/filesharing/%Y/%m/%d/')
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    # Отметка времени, когда будет удалён файл
    time_delete = models.DateTimeField()

    password_for_delete = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )
    password_for_download = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )

    pub_date = models.DateTimeField(auto_now=True)
    creator_ip = models.CharField(max_length=15)

    hints = GenericRelation(Hint, related_name="files")
    download = GenericRelation(Download, related_name="files")

    def get_absolute_url(self):
        return reverse('filesharing:file', args={self.id})
