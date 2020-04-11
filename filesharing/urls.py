from django.conf.urls import url, include

from filesharing import views

app_name = "shorturl"

urlpatterns = [
    url(r'^$', views.upload, name="index"),
    url(r'^files/(?P<file>.*)/$', views.upload, name="file"),
    #url(r'^(?P<hash>\w{10})/$', views.redirect),
]
