import json

from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from apps.analytics.services import log_event
from apps.categories.models import Category

from .models import Product


def _apply_filters(request, queryset):
    category_slug = request.GET.get("category")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    min_rating = request.GET.get("rating")
    sort = request.GET.get("sort", "relevancia")

    category = None
    if category_slug:
        category = Category.objects.filter(slug=category_slug, is_active=True).first()
        if category:
            queryset = queryset.filter(category=category)

    if min_price:
        try:
            queryset = queryset.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            queryset = queryset.filter(price__lte=float(max_price))
        except ValueError:
            pass
    if min_rating:
        try:
            queryset = queryset.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    sort_map = {
        "price_asc": "price",
        "price_desc": "-price",
        "recientes": "-created_at",
    }
    if sort in sort_map:
        queryset = queryset.order_by(sort_map[sort])
    # "relevancia" keeps the model's default ordering (featured first, then name)

    return queryset, category, sort


def product_list(request):
    query = request.GET.get("q", "").strip()
    queryset = Product.objects.filter(is_active=True).select_related("category")

    if query:
        queryset = queryset.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(short_description__icontains=query)
            | Q(category__name__icontains=query)
            | Q(asin__iexact=query)
        )
        log_event(request, "search", metadata={"q": query})

    queryset, category, sort = _apply_filters(request, queryset)

    return render(
        request,
        "products/list.html",
        {
            "products": queryset,
            "categories": Category.objects.filter(is_active=True),
            "category": category,
            "query": query,
            "sort": sort,
            "result_count": queryset.count(),
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category"), slug=slug, is_active=True
    )
    related = (
        Product.objects.filter(category=product.category, is_active=True)
        .exclude(id=product.id)
        .select_related("category")[:4]
    )
    log_event(request, "product_view", product=product)

    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "description": product.short_description or product.description,
        "sku": product.asin,
    }
    if product.display_image:
        data["image"] = product.display_image
    if product.rating:
        data["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(product.rating),
            "reviewCount": str(product.review_count),
        }
    if product.price:
        data["offers"] = {
            "@type": "Offer",
            "priceCurrency": product.currency,
            "price": str(product.price),
            "availability": "https://schema.org/InStock",
            "url": f"{settings.SITE_URL}{reverse('affiliate:go', args=[product.slug])}",
        }

    return render(
        request,
        "products/detail.html",
        {
            "product": product,
            "related": related,
            "product_jsonld": json.dumps(data),
        },
    )
