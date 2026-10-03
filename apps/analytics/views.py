from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.utils import timezone

from .models import Event


@staff_member_required
def dashboard(request):
    since = timezone.now() - timedelta(days=30)
    clicks = Event.objects.filter(event_type=Event.EventType.AMAZON_CLICK, created_at__gte=since)

    top_products = (
        clicks.values("product__name").annotate(total=Count("id")).order_by("-total")[:10]
    )
    clicks_by_day = (
        clicks.annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Count("id"))
        .order_by("-day")[:14]
    )
    totals_by_type = (
        Event.objects.filter(created_at__gte=since)
        .values("event_type")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    return render(
        request,
        "analytics/dashboard.html",
        {
            "top_products": top_products,
            "clicks_by_day": clicks_by_day,
            "totals_by_type": totals_by_type,
        },
    )
