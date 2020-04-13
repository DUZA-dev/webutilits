from hashlib import md5
from datetime import timedelta, datetime
from django.utils import timezone

from django.test import TestCase

from .views import *
from .models import Url


URLS = [
    'https://soundcloud.com/discover',
    'http://meduza.io/',
    'tg://asd.asd'
]


class TestCreateUrls(TestCase):
    def test_call_view_load(self):
        response = self.client.get('/shorturl/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shorturl.html')

    def test_call_view_on_create_url_object(self):
        for url in URLS:
            response = self.client.post('/shorturl/', {'url': url})
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'shorturl.html')

    def test_call_view_on_redirect_page(self):
        for url in URLS:
            response = self.client.post('/shorturl/', {'url': url})
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'shorturl.html')

            response = self.client.get(response.context['url'], follow=True)
            self.assertEqual(response.status_code, 200)

    def test_call_view_on_redirect_page_error(self):
        for url in ['123', 'sdfdsf']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
