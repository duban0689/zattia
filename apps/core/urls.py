from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("contacto/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("privacidad/", views.privacidad, name="privacidad"),
    path("terminos/", views.terminos, name="terminos"),
    path("cookies/", views.cookies, name="cookies"),
    path("aviso-afiliados/", views.aviso_afiliados, name="aviso_afiliados"),
]
