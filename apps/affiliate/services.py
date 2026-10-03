"""Centralized Amazon affiliate link building and click tracking.

Keeping this in one place (instead of the affiliate tag being hardcoded
into templates) means the tag, marketplace, or link format can change in
one spot without touching every template.
"""

from urllib.parse import urlencode, urlparse

from django.conf import settings


def _domain_from_marketplace(marketplace: str | None = None) -> str:
    return (marketplace or settings.AMAZON_MARKETPLACE or "amazon.com").strip()


def build_amazon_affiliate_url(product) -> str:
    """Build a single-product Amazon affiliate link for `product`
    (an apps.products.models.Product instance)."""
    if not product or not product.asin:
        raise ValueError(
            "No se puede construir un enlace de afiliado sin un producto con ASIN válido."
        )

    domain = _domain_from_marketplace()
    base = f"https://www.{domain}/dp/{product.asin}"

    params = {"tag": settings.AMAZON_AFFILIATE_TAG}

    # If a full amazon_url override was provided on the product, merge our
    # tag into it instead of discarding it, but avoid duplicating `tag`.
    if product.amazon_url:
        parsed = urlparse(product.amazon_url)
        if parsed.scheme and parsed.netloc:
            base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    return f"{base}?{urlencode(params)}"


def build_amazon_cart_url(cart_items, marketplace: str | None = None) -> str | None:
    """Build a single Amazon 'remote shopping cart' link that adds every
    item from `cart_items` (as returned by apps.cart.services.Cart.get_cart)
    into the visitor's real Amazon cart at once."""
    if not cart_items:
        return None

    domain = _domain_from_marketplace(marketplace)
    params = [("AssociateTag", settings.AMAZON_AFFILIATE_TAG)]
    i = 0
    for item in cart_items:
        product = item["product"]
        if not product.asin:
            continue
        i += 1
        params.append((f"ASIN.{i}", product.asin))
        params.append((f"Quantity.{i}", str(item["quantity"])))

    if i == 0:
        return None
    return f"https://www.{domain}/gp/aws/cart/add.html?{urlencode(params)}"


def track_affiliate_click(request, product):
    from .models import AffiliateClick

    return AffiliateClick.objects.create(
        product=product,
        referrer=request.META.get("HTTP_REFERER", "")[:500],
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        session_key=request.session.session_key or "",
    )
