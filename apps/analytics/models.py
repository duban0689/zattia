from django.db import models


class Event(models.Model):
    class EventType(models.TextChoices):
        PRODUCT_VIEW = "product_view", "Vista de producto"
        SEARCH = "search", "Búsqueda"
        ADD_TO_CART = "add_to_cart", "Agregar al carrito"
        REMOVE_FROM_CART = "remove_from_cart", "Quitar del carrito"
        AMAZON_CLICK = "amazon_click", "Clic a Amazon"

    event_type = models.CharField(max_length=30, choices=EventType.choices)
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    session_key = models.CharField(max_length=60, blank=True)
    metadata = models.JSONField(blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        indexes = [
            models.Index(fields=["event_type", "created_at"]),
        ]

    def __str__(self):
        return f"{self.get_event_type_display()} — {self.created_at:%Y-%m-%d %H:%M}"
