from django.conf.urls import url, include

from rest_framework import routers

from shorturl import views

app_name = "shorturl"

router = routers.DefaultRouter()
router.register(r'urls', views.UrlViewSet)
router.register(r'protocols', views.ProtocolViewSet)

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<hash>\w{10})/$', views.redirect),

    url(r'^api/', include(router.urls)),
]
