"""Session-backed shopping cart. Works for anonymous users — no account
required. Only product ids and quantities are stored in the session; no
payment, card, or personal information is ever stored here."""

from apps.products.models import Product

SESSION_KEY = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(SESSION_KEY)
        if cart is None:
            cart = {}
            self.session[SESSION_KEY] = cart
        self.cart = cart

    def add_product(self, product: Product, quantity: int = 1):
        if not product.is_active:
            return
        pid = str(product.id)
        self.cart[pid] = self.cart.get(pid, 0) + max(quantity, 1)
        self._save()

    def remove_product(self, product: Product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self._save()

    def update_quantity(self, product: Product, quantity: int):
        pid = str(product.id)
        if quantity <= 0:
            self.remove_product(product)
            return
        self.cart[pid] = quantity
        self._save()

    def clear_cart(self):
        self.session[SESSION_KEY] = {}
        self._save()

    def get_cart(self):
        """Returns a list of {product, quantity, subtotal} for valid, active
        products currently in the cart — silently drops ids for products
        that no longer exist or were deactivated."""
        ids = self.cart.keys()
        products = {str(p.id): p for p in Product.objects.filter(id__in=ids, is_active=True)}
        items = []
        for pid, quantity in self.cart.items():
            product = products.get(pid)
            if not product:
                continue
            subtotal = (product.price or 0) * quantity
            items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
        return items

    def total_quantity(self) -> int:
        return sum(self.cart.values())

    def estimated_subtotal(self):
        return sum(item["subtotal"] for item in self.get_cart())

    def _save(self):
        self.session[SESSION_KEY] = self.cart
        self.session.modified = True

    def __len__(self):
        return self.total_quantity()

    def __iter__(self):
        return iter(self.get_cart())
