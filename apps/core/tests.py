from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class CorePagesTests(TestCase):
    def test_home_200(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    def test_faq_200(self):
        response = self.client.get(reverse("core:faq"))
        self.assertEqual(response.status_code, 200)

    def test_legal_pages_200(self):
        for name in ["privacidad", "terminos", "cookies", "aviso_afiliados"]:
            response = self.client.get(reverse(f"core:{name}"))
            self.assertEqual(response.status_code, 200, f"{name} debería responder 200")


class ContactFormTests(TestCase):
    def test_valid_submission_creates_message_and_redirects(self):
        response = self.client.post(
            reverse("core:contact"),
            {
                "name": "Test",
                "email": "test@example.com",
                "message": "Hola",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_invalid_submission_shows_errors(self):
        response = self.client.post(
            reverse("core:contact"),
            {"name": "", "email": "no-es-correo", "message": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
