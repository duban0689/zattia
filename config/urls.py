from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from apps.categories.sitemaps import CategorySitemap
from apps.products.sitemaps import ProductSitemap

sitemaps = {
    "products": ProductSitemap,
    "categories": CategorySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("", include("apps.products.urls")),
    path("", include("apps.categories.urls")),
    path("carrito/", include("apps.cart.urls")),
    path("go/", include("apps.affiliate.urls")),
    path("analytics/", include("apps.analytics.urls")),
    path("api/", include("apps.products.api_urls")),
    path("api/", include("apps.categories.api_urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
