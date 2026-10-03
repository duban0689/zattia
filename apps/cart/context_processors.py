from .services import Cart


def cart(request):
    c = Cart(request)
    return {"cart_count": c.total_quantity()}
