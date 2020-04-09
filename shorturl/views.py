import time
import hashlib

from django.utils.html import escape
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets

from core.models import Hint
from shorturl.models import Url, Protocol
from shorturl.forms import ShortenerUrlForm
from shorturl.serializers import UrlSerializer, ProtocolSerializer


def get_client_ip(request):
    # Получаем ip-адрес пользователя/отправителя
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    context = dict()
    form = ShortenerUrlForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        protocol, url = form.cleaned_data['url']

        # Хэширую URL с солью в виде нынешнего времени, для последующего
        # формирования короткой ссылки.
        short_url = hashlib.md5(
            "".join([url, str(time.time())]).encode('utf8')
        ).hexdigest()[:10]

        protocol, c = Protocol.objects.get_or_create(protocol=protocol)

        url, c = Url.objects.get_or_create(
            url=escape(url),
            url_short=short_url,
            protocol=protocol,
            defaults={'creator_ip': get_client_ip(request)}
        )

        context['url'] = url
    context['form'] = form
    return render(request, 'index.html', context=context)


def redirect(request, hash):
    url = get_object_or_404(Url, url_short=hash)
    Hint(content_object=url, ip=get_client_ip(request)).save()

    return HttpResponse(
        '<script>window.location.href = "%s://%s";</script>' % (url.protocol.protocol, url.url)
    )


class ProtocolViewSet(viewsets.ModelViewSet):
    queryset = Protocol.objects.all().order_by('-pub_date')
    serializer_class = ProtocolSerializer


class UrlViewSet(viewsets.ModelViewSet):
    queryset = Url.objects.all().order_by('-pub_date')
    serializer_class = UrlSerializer
