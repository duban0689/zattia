from django.test import Client, TestCase
from django.urls import reverse

from apps.categories.models import Category
from apps.products.models import Product

from .services import Cart


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


class CartServiceTests(TestCase):
    def setUp(self):
        self.product = make_product()

    def _cart(self, request):
        request.session.save()
        return Cart(request)

    def test_add_and_total(self):
        request = self.client.request().wsgi_request
        cart = self._cart(request)
        cart.add_product(self.product, quantity=2)
        self.assertEqual(cart.total_quantity(), 2)

    def test_update_to_zero_removes(self):
        request = self.client.request().wsgi_request
        cart = self._cart(request)
        cart.add_product(self.product)
        cart.update_quantity(self.product, 0)
        self.assertEqual(cart.total_quantity(), 0)

    def test_inactive_product_not_added(self):
        inactive = make_product(asin="B0DEMO0002", slug="inactivo", is_active=False)
        request = self.client.request().wsgi_request
        cart = self._cart(request)
        cart.add_product(inactive)
        self.assertEqual(cart.total_quantity(), 0)


class CartViewTests(TestCase):
    def setUp(self):
        self.product = make_product()

    def test_empty_cart_detail(self):
        response = self.client.get(reverse("cart:detail"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["cart_items"], [])

    def test_add_then_appears_in_cart(self):
        self.client.post(reverse("cart:add", args=[self.product.id]))
        response = self.client.get(reverse("cart:detail"))
        self.assertEqual(len(response.context["cart_items"]), 1)

    def test_remove(self):
        self.client.post(reverse("cart:add", args=[self.product.id]))
        self.client.post(reverse("cart:remove", args=[self.product.id]))
        response = self.client.get(reverse("cart:detail"))
        self.assertEqual(len(response.context["cart_items"]), 0)

    def test_add_endpoint_rejects_get(self):
        response = self.client.get(reverse("cart:add", args=[self.product.id]))
        self.assertEqual(response.status_code, 405)

    def test_post_without_csrf_token_rejected(self):
        strict_client = Client(enforce_csrf_checks=True)
        response = strict_client.post(reverse("cart:add", args=[self.product.id]))
        self.assertEqual(response.status_code, 403)

    def test_add_json_response(self):
        response = self.client.post(
            reverse("cart:add", args=[self.product.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["cart_count"], 1)
