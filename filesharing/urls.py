from django.conf.urls import url

from filesharing import views

app_name = "filesharing"



urlpatterns = [
    url(r'^files/delete/(?P<file_id>\d*)/$', views.delete, name="delete"),
    url(r'^files/download/(?P<file_id>\d*)/$', views.download, name="download"),
    url(r'^files/(?P<file_id>\d*)/$', views.file, name="file"),
    url(r'^$', views.upload, name="index"),
]
