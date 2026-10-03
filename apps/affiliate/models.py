from django.db import models

from apps.products.models import Product


class AffiliateClick(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="affiliate_clicks")
    created_at = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=500, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    session_key = models.CharField(max_length=60, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Clic a Amazon"
        verbose_name_plural = "Clics a Amazon"

    def __str__(self):
        return f"{self.product.name} — {self.created_at:%Y-%m-%d %H:%M}"
