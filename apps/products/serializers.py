from rest_framework import serializers

from apps.categories.serializers import CategorySerializer

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    affiliate_url = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            "id",
            "asin",
            "name",
            "slug",
            "category",
            "short_description",
            "description",
            "price",
            "currency",
            "rating",
            "review_count",
            "image_url",
            "is_featured",
            "is_demo_data",
            "affiliate_url",
        ]
