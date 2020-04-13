from django.db import models
from django.urls import reverse


class Note(models.Model):
    # Модель, кранящая сведения об опубликованном файле и путь до него
    note = models.TextField()

    # Отметка времени, когда будет удалён файл
    time_delete = models.DateTimeField()

    password_for_read = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )

    pub_date = models.DateTimeField(auto_now=True)
    creator_ip = models.CharField(max_length=15)

    url = models.CharField(max_length=32)

    def get_absolute_url(self):
        return reverse('privatenote:note', args={self.url})
