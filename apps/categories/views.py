from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import Category


def category_detail(request, slug):
    """Friendly entry point for a category — delegates to the shared
    products list/filter view so sorting and filtering stay consistent
    everywhere, instead of duplicating that logic here."""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    return redirect(f"{reverse('products:product_list')}?category={category.slug}")
