"""webutilits URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps import views   # Представление


from core.sitemap import HomeSitemap, sitemap_filesharing
from core import views as core

handler404 = "core.views.handler404"

sitemaps = {
    "home": HomeSitemap,
    "filesharing": GenericSitemap(sitemap_filesharing, priority=0.5),
}


urlpatterns = [
    url(
        r'^sitemap\.xml$',
        cache_page(86400)(views.index),
        {'sitemaps': sitemaps}
    ),
    url(
        r'^sitemap-(?P<section>\w+)\.xml$',
        cache_page(86400)(views.sitemap),
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),

    url('^privatenotes/', include('privatenote.urls', namespace='privatenote')),
    url('^filesharing/', include('filesharing.urls', namespace='filesharing')),
    url('^shorturl/', include('shorturl.urls', namespace='shorturl')),

    url('^$', core.index),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
