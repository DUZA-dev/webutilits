from django.conf.urls import url

from shorturl import views

app_name = "shorturl"


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<hash>\w{10})/$', views.redirect, name="shorturl"),
]
