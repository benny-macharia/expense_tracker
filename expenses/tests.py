from django.test import TestCase

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view_GET(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/register.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)
