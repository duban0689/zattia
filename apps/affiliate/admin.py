from django.contrib import admin

from .models import AffiliateClick


@admin.register(AffiliateClick)
class AffiliateClickAdmin(admin.ModelAdmin):
    # Clics por producto: usa el buscador o filtra por producto desde aquí.
    # Clics por día: usa el desglose por fecha (date_hierarchy) de arriba.
    list_display = ("product", "created_at", "session_key")
    list_filter = ("created_at", "product")
    search_fields = ("product__name", "product__asin")
    readonly_fields = ("product", "created_at", "referrer", "user_agent", "session_key")
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False
