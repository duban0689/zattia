from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("agregar/<int:product_id>/", views.cart_add, name="add"),
    path("eliminar/<int:product_id>/", views.cart_remove, name="remove"),
    path("actualizar/<int:product_id>/", views.cart_update, name="update"),
    path("vaciar/", views.cart_clear, name="clear"),
]
