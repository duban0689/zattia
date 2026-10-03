from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("productos/", views.product_list, name="product_list"),
    path("buscar/", views.product_list, name="search"),
    path("producto/<slug:slug>/", views.product_detail, name="product_detail"),
]
