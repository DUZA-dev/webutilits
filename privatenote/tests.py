from hashlib import md5
from datetime import timedelta, datetime
from django.utils import timezone

from django.test import TestCase

from .views import *
from .models import Note
# Create your tests here.

NOTES = [
    'криптографически-небезопасный PRNG в Питоне, поэтому если вы его используете в контексте, где не желательно, чтобы можно было угадать результат последовательных вызовов, например, при генерации паролей, то следует использовать CSPRNG',
    'I have edit and create form and I would like to have this clean in one place but not copy to 2 views.',
    't = ClientForm(request.POST, prefix="client")if form_user.is_valid() and form_client.is_valid():obj_user = form_user.save(commit=False)obj_client = form_client.save(commi',
    '<p>I speak on python</p>'
]

PASSWORDS = [
    'asdkasdklajsd',
    'iwoerjweoirj',
    '123891238JnnsjdfIIjansdasd',
    ''
]

NOTES_URL = [
    'a',
    '123',
    '90177158a7abb3d44b87f45288a50bds'
]


class TestCreateNotes(TestCase):
    def test_call_view_load(self):
        response = self.client.get('/privatenotes/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'privatenote/create.html')

    def test_call_view_post_create_note(self):
        for note in NOTES:
            for password in PASSWORDS:
                response = self.client.post(
                    '/privatenotes/',
                    {'note': note, 'password': password},
                )
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'privatenote/create.html')


class TestNotes(TestCase):
    def setUp(self):
        self.passwords = {}
        for note in NOTES:
            for password in PASSWORDS:
                hash_password = md5(password.encode("utf8")).hexdigest()
                self.passwords[hash_password] = password
                Note(
                    note=note,
                    password_for_read=md5(password.encode("utf8")).hexdigest(),
                    creator_ip="127.0.0.1",
                    time_delete=datetime.now(tz=timezone.utc) + timedelta(days=7),
                    url=md5("".join([
                        str(datetime.now())
                    ]).encode("utf8")).hexdigest()
                ).save()

    def test_call_view_load(self):
        for note in Note.objects.all():
            response = self.client.get('/privatenotes/%s/' % note.url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'privatenote/note.html')

    def test_call_view_fail_invalid(self):
        for url in NOTES_URL:
            response = self.client.get('/privatenotes/%s/' % url)
            self.assertEqual(response.status_code, 404)

    def test_call_ajax(self):
        for note in Note.objects.all():
            context = {}
            if note.password_for_read:
                context["password"] = self.passwords[note.password_for_read]

            response = self.client.post(
                '/privatenotes/%s/' % note.url,
                context,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            self.assertEqual(response.status_code, 200)
            self.assertEquals('application/json', response['Content-Type'])
