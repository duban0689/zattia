from django.db import models
from django.urls import reverse

from apps.categories.models import Category


class Product(models.Model):
    asin = models.CharField(
        "ASIN",
        max_length=20,
        unique=True,
        help_text="Código de producto en Amazon, ej. B0CTEST123",
    )
    name = models.CharField("Nombre", max_length=200)
    slug = models.SlugField("Slug", max_length=220, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Categoría",
    )

    short_description = models.CharField("Descripción corta", max_length=240, blank=True)
    description = models.TextField("Descripción", blank=True)
    features = models.TextField(
        "Características",
        blank=True,
        help_text="Una característica por línea.",
    )

    price = models.DecimalField(
        "Precio referencial", max_digits=10, decimal_places=2, null=True, blank=True
    )
    original_price = models.DecimalField(
        "Precio original (tachado)", max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Opcional. Si es mayor al precio actual, se muestra tachado con el % de descuento, como en Amazon.",
    )
    currency = models.CharField("Moneda", max_length=6, default="USD")

    rating = models.DecimalField(
        "Calificación", max_digits=2, decimal_places=1, null=True, blank=True
    )
    review_count = models.PositiveIntegerField("Número de reseñas", default=0)

    image = models.ImageField("Imagen principal", upload_to="products/", blank=True, null=True)
    image_url = models.URLField(
        "URL de imagen externa",
        max_length=500,
        blank=True,
        help_text="Alternativa si no subes una imagen (ej. tomada de Amazon).",
    )

    amazon_url = models.URLField(
        "URL de producto en Amazon",
        max_length=500,
        blank=True,
        help_text="Opcional — si se deja vacío, se construye automáticamente desde el ASIN.",
    )

    is_demo_data = models.BooleanField(
        "Es dato de demostración",
        default=True,
        help_text="Marca productos de ejemplo que no provienen de datos reales de Amazon.",
    )
    is_active = models.BooleanField("Activo", default=True)
    is_featured = models.BooleanField("Destacado", default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "name"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:product_detail", args=[self.slug])

    @property
    def feature_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]

    @property
    def discount_percent(self):
        if not self.price or not self.original_price or self.original_price <= self.price:
            return None
        return round((1 - (self.price / self.original_price)) * 100)

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url

    @property
    def affiliate_url(self):
        from apps.affiliate.services import build_amazon_affiliate_url

        return build_amazon_affiliate_url(self)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField("Imagen", upload_to="products/gallery/", blank=True, null=True)
    image_url = models.URLField("URL de imagen externa", max_length=500, blank=True)
    order = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Imagen adicional"
        verbose_name_plural = "Imágenes adicionales"

    def __str__(self):
        return f"Imagen de {self.product.name} #{self.order}"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url
