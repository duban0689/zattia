from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "product", "created_at", "session_key")
    list_filter = ("event_type", "created_at")
    search_fields = ("product__name", "session_key")
    date_hierarchy = "created_at"
    readonly_fields = ("event_type", "product", "session_key", "metadata", "created_at")

    def has_add_permission(self, request):
        return False
