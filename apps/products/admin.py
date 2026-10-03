from django.contrib import admin

from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "asin",
        "price",
        "rating",
        "is_featured",
        "is_active",
        "is_demo_data",
    )
    list_filter = ("category", "is_active", "is_featured", "is_demo_data")
    search_fields = ("name", "asin", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-is_featured", "name")
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProductImageInline]
    fieldsets = (
        (
            "Información básica",
            {
                "fields": ("name", "slug", "category", "asin", "amazon_url"),
            },
        ),
        (
            "Contenido",
            {
                "fields": ("short_description", "description", "features"),
            },
        ),
        (
            "Precio y reputación",
            {
                "fields": ("price", "original_price", "currency", "rating", "review_count"),
            },
        ),
        (
            "Imagen",
            {
                "fields": ("image", "image_url"),
            },
        ),
        (
            "Estado",
            {
                "fields": ("is_active", "is_featured", "is_demo_data"),
            },
        ),
        (
            "Auditoría",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
    actions = ["mark_active", "mark_inactive", "mark_featured", "unmark_featured"]

    @admin.action(description="Activar productos seleccionados")
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Desactivar productos seleccionados")
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Marcar como destacados")
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Quitar de destacados")
    def unmark_featured(self, request, queryset):
        queryset.update(is_featured=False)
