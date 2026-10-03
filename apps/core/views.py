import json

from django.contrib import messages
from django.shortcuts import redirect, render

from apps.categories.models import Category
from apps.products.models import Product

from .forms import ContactForm


def home(request):
    categories = Category.objects.filter(is_active=True)
    featured = Product.objects.filter(is_active=True, is_featured=True).select_related("category")[
        :8
    ]
    popular = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .order_by("-review_count")[:8]
    )
    recent = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .order_by("-created_at")[:8]
    )
    return render(
        request,
        "core/home.html",
        {
            "categories": categories,
            "featured": featured,
            "popular": popular,
            "recent": recent,
        },
    )


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Gracias por escribirnos, te responderemos pronto.")
            return redirect("core:contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


def faq(request):
    questions = [
        (
            "¿Qué es este sitio?",
            "Zattia es una plataforma de descubrimiento de productos: seleccionamos recomendaciones por categoría para ayudarte a decidir más rápido.",
        ),
        (
            "¿Dónde compro los productos?",
            "La compra final siempre se realiza en Amazon. Zattia no procesa pagos ni almacena información financiera.",
        ),
        (
            "¿El sitio procesa pagos?",
            "No. Zattia nunca solicita ni guarda tarjetas, datos bancarios ni contraseñas de pago. Todo el pago ocurre en Amazon.",
        ),
        (
            "¿Cómo funciona el carrito?",
            "Agregas productos a un carrito temporal guardado en tu sesión del navegador. Al continuar, se te redirige a Amazon con esos mismos productos.",
        ),
        (
            "¿Por qué me redirige a Amazon?",
            "Porque ahí se completa la compra real, de forma segura, con tus propios métodos de pago.",
        ),
        (
            "¿Los precios pueden cambiar?",
            "Sí. Los precios mostrados en Zattia son referenciales; el precio final y la disponibilidad los define Amazon al momento de tu compra.",
        ),
        (
            "¿Cómo funciona la afiliación?",
            "Zattia participa en el Programa de Afiliados de Amazon. Al comprar a través de nuestros enlaces, Amazon nos paga una comisión, sin costo adicional para ti.",
        ),
    ]
    faq_jsonld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in questions
            ],
        }
    )
    return render(request, "core/faq.html", {"questions": questions, "faq_jsonld": faq_jsonld})


def privacidad(request):
    return render(request, "core/privacidad.html")


def terminos(request):
    return render(request, "core/terminos.html")


def cookies(request):
    return render(request, "core/cookies.html")


def aviso_afiliados(request):
    return render(request, "core/aviso_afiliados.html")
