from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Nombre", max_length=80)
    slug = models.SlugField("Slug", max_length=90, unique=True)
    description = models.CharField("Descripción", max_length=240, blank=True)
    image = models.ImageField("Imagen", upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField("Activa", default=True)
    order = models.PositiveIntegerField("Orden", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:product_list") + f"?category={self.slug}"
