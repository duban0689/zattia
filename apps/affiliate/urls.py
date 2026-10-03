from django.urls import path

from . import views

app_name = "affiliate"

urlpatterns = [
    path("<slug:slug>/", views.go_to_amazon, name="go"),
]
