from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):

    def test_home(self):
        # Test the home page loading
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_privacy_notice_view(self):
        # Test the privacy notice page
        url = reverse('privacy_notice')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/privacy_notice.html')
