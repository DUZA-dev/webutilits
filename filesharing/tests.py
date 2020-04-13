from django.test import TestCase

class TestFilesharingUrls(TestCase):
    def test_call_view_load(self):
        response = self.client.get('/filesharing/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'filesharing/upload.html')
