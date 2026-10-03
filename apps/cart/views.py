from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.affiliate.services import build_amazon_cart_url
from apps.analytics.services import log_event
from apps.products.models import Product

from .services import Cart


def _wants_json(request):
    return request.headers.get(
        "x-requested-with"
    ) == "XMLHttpRequest" or "application/json" in request.headers.get("accept", "")


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = Cart(request)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1
    cart.add_product(product, quantity=quantity)
    log_event(request, "add_to_cart", product=product, metadata={"quantity": quantity})

    if _wants_json(request):
        return JsonResponse(
            {
                "ok": True,
                "cart_count": cart.total_quantity(),
                "message": "Producto agregado al carrito.",
            }
        )

    messages.success(request, "Producto agregado al carrito.")
    next_url = request.POST.get("next") or product.get_absolute_url()
    return redirect(next_url)


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove_product(product)

    if _wants_json(request):
        return JsonResponse(
            {
                "ok": True,
                "cart_count": cart.total_quantity(),
                "message": "Producto eliminado del carrito.",
            }
        )

    messages.info(request, "Producto eliminado del carrito.")
    return redirect("cart:detail")


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1
    cart.update_quantity(product, quantity)

    if _wants_json(request):
        return JsonResponse({"ok": True, "cart_count": cart.total_quantity()})

    messages.success(request, "Carrito actualizado.")
    return redirect("cart:detail")


@require_POST
def cart_clear(request):
    Cart(request).clear_cart()
    if _wants_json(request):
        return JsonResponse({"ok": True, "cart_count": 0})
    messages.info(request, "Carrito vaciado.")
    return redirect("cart:detail")


def cart_detail(request):
    cart = Cart(request)
    items = cart.get_cart()
    amazon_cart_url = build_amazon_cart_url(items) if items else None
    return render(
        request,
        "cart/detail.html",
        {
            "cart_items": items,
            "amazon_cart_url": amazon_cart_url,
            "subtotal": cart.estimated_subtotal(),
        },
    )
