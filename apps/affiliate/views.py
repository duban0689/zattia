from django.shortcuts import get_object_or_404, render

from apps.analytics.services import log_event
from apps.products.models import Product

from .services import build_amazon_affiliate_url, track_affiliate_click


def go_to_amazon(request, slug):
    """Transparent redirect to Amazon for a given product, via its
    affiliate link. The visitor lands on a brief interstitial (auto-advances,
    but also shows a visible link) so it's always clear they're being sent
    to Amazon — never a silent/hidden redirect."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    affiliate_url = build_amazon_affiliate_url(product)
    track_affiliate_click(request, product)
    log_event(request, "amazon_click", product=product)

    return render(
        request,
        "affiliate/redirecting.html",
        {
            "product": product,
            "affiliate_url": affiliate_url,
        },
    )
