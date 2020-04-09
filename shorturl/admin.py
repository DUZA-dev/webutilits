from django.contrib import admin

from core.models import Hint
from shorturl import models


@admin.register(models.Url)
class UrlAdmin(admin.ModelAdmin):
    # Определяет вид в сокращенных ссылок в админке

    date_hierarchy = 'pub_date'
    list_display = (
        'url_short',
        'protocol',
        'url',
        'creator_ip',
        'pub_date',
        'jumps'
    )

    def jumps(self, obj):
        # Возвращает кол-во перенаправленных пользователей
        return obj.hints.count()


admin.site.register(models.Protocol)
