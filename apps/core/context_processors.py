from django.conf import settings


def site(request):
    from apps.categories.models import Category

    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_URL": settings.SITE_URL,
        "GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID,
        "nav_categories": Category.objects.filter(is_active=True),
    }
