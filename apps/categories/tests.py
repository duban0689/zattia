from django.test import TestCase
from django.urls import reverse

from .models import Category


class CategoryModelTests(TestCase):
    def test_str_and_slug(self):
        cat = Category.objects.create(name="Tecnología", slug="tecnologia")
        self.assertEqual(str(cat), "Tecnología")
        self.assertIn("category=tecnologia", cat.get_absolute_url())


class CategoryViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Hogar", slug="hogar")

    def test_category_detail_redirects_to_filtered_list(self):
        response = self.client.get(reverse("categories:category_detail", args=["hogar"]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("category=hogar", response.url)

    def test_inactive_category_404(self):
        self.category.is_active = False
        self.category.save()
        response = self.client.get(reverse("categories:category_detail", args=["hogar"]))
        self.assertEqual(response.status_code, 404)
