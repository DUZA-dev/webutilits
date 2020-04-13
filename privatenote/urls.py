from django.conf.urls import url

from privatenote import views

app_name = "privatenote"

urlpatterns = [
    url(r'^(?P<note>\w{32})/$', views.note, name="note"),
    url(r'^$', views.index, name="index"),
]
