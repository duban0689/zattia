from django.test import TestCase
from django.urls import reverse

from apps.categories.models import Category

from .models import Product


def make_product(**kwargs):
    category, _ = Category.objects.get_or_create(slug="tecnologia", defaults={"name": "Tecnología"})
    defaults = {
        "asin": "B0DEMO0001",
        "name": "Producto demo",
        "slug": "producto-demo",
        "category": category,
        "price": 10,
        "is_active": True,
    }
    defaults.update(kwargs)
    return Product.objects.create(**defaults)


class ProductModelTests(TestCase):
    def test_affiliate_url_contains_tag_and_asin(self):
        product = make_product()
        url = product.affiliate_url
        self.assertIn(product.asin, url)
        self.assertIn("tag=", url)

    def test_feature_list_splits_lines(self):
        product = make_product(features="Uno\nDos\n\nTres")
        self.assertEqual(product.feature_list, ["Uno", "Dos", "Tres"])


class ProductDetailViewTests(TestCase):
    def test_detail_200_for_active_product(self):
        product = make_product()
        response = self.client.get(reverse("products:product_detail", args=[product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.name)

    def test_detail_404_for_inactive_product(self):
        product = make_product(is_active=False)
        response = self.client.get(reverse("products:product_detail", args=[product.slug]))
        self.assertEqual(response.status_code, 404)


class ProductSearchTests(TestCase):
    def test_search_finds_by_name(self):
        make_product(name="Audífonos inalámbricos", slug="audifonos")
        make_product(asin="B0DEMO0002", name="Silla de oficina", slug="silla-oficina")
        response = self.client.get(reverse("products:search"), {"q": "audífonos"})
        self.assertContains(response, "Audífonos inalámbricos")
        self.assertNotContains(response, "Silla de oficina")

    def test_empty_search_shows_all_active(self):
        make_product()
        response = self.client.get(reverse("products:product_list"))
        self.assertEqual(response.context["result_count"], 1)

    def test_filter_by_category(self):
        other_cat = Category.objects.create(slug="hogar", name="Hogar")
        make_product()
        make_product(asin="B0DEMO0003", slug="otro", category=other_cat)
        response = self.client.get(reverse("products:product_list"), {"category": "hogar"})
        self.assertEqual(response.context["result_count"], 1)

    def test_filter_by_price_range(self):
        make_product(price=10)
        make_product(asin="B0DEMO0004", slug="caro", price=1000)
        response = self.client.get(reverse("products:product_list"), {"min_price": "500"})
        self.assertEqual(response.context["result_count"], 1)
