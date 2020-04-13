from django.contrib import sitemaps
from django.urls import reverse

from filesharing.models import File

sitemap_filesharing = {
    'queryset': File.objects.all(),
}


class HomeSitemap(sitemaps.Sitemap):
    priority = 0.5         # Приоритет
    changefreq = 'daily'   # Частота проверки

    # Метод, возвращающий массив с url-ками
    def items(self):
        return ['privatenote:index',
                'filesharing:index',
                'shorturl:index',
                ]

    # Метод непосредственной экстракции url из шаблонаs
    def location(self, item):
        return reverse(item)
