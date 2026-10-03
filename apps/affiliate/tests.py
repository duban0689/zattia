from django.test import TestCase
from django.urls import reverse

from apps.categories.models import Category
from apps.products.models import Product

from .models import AffiliateClick
from .services import build_amazon_affiliate_url, build_amazon_cart_url


def make_product(**kwargs):
    category, _ = Category.objects.get_or_create(slug="tecnologia", defaults={"name": "Tecnología"})
    defaults = dict(
        asin="B0DEMO0001",
        name="Producto demo",
        slug="producto-demo",
        category=category,
        price=10,
        is_active=True,
    )
    defaults.update(kwargs)
    return Product.objects.create(**defaults)


class BuildAffiliateUrlTests(TestCase):
    def test_contains_asin_and_tag_once(self):
        product = make_product()
        url = build_amazon_affiliate_url(product)
        self.assertIn(product.asin, url)
        self.assertEqual(url.count("tag="), 1)

    def test_raises_without_asin(self):
        product = make_product(asin="")
        with self.assertRaises(ValueError):
            build_amazon_affiliate_url(product)


class BuildCartUrlTests(TestCase):
    def test_multiple_items_all_present(self):
        p1 = make_product()
        p2 = make_product(asin="B0DEMO0002", slug="otro")
        items = [{"product": p1, "quantity": 2}, {"product": p2, "quantity": 1}]
        url = build_amazon_cart_url(items)
        self.assertIn(p1.asin, url)
        self.assertIn(p2.asin, url)
        self.assertIn("AssociateTag=", url)

    def test_empty_cart_returns_none(self):
        self.assertIsNone(build_amazon_cart_url([]))


class GoToAmazonViewTests(TestCase):
    def test_redirect_endpoint_tracks_click(self):
        product = make_product()
        response = self.client.get(reverse("affiliate:go", args=[product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AffiliateClick.objects.filter(product=product).count(), 1)
        self.assertContains(response, "amazon")

    def test_inactive_product_404(self):
        product = make_product(is_active=False)
        response = self.client.get(reverse("affiliate:go", args=[product.slug]))
        self.assertEqual(response.status_code, 404)
