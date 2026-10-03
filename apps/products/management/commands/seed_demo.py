from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.categories.models import Category
from apps.products.models import Product

CATEGORIES = [
    ("Tecnología", "tecnologia", "Gadgets y dispositivos para el día a día."),
    ("Gaming", "gaming", "Todo para armar o mejorar tu setup de videojuegos."),
    ("Hogar", "hogar", "Productos para hacer tu casa más cómoda."),
    ("Cocina", "cocina", "Herramientas y electrodomésticos de cocina."),
    ("Oficina", "oficina", "Equipo para trabajar mejor desde casa o la oficina."),
    ("Fitness", "fitness", "Equipo y accesorios para entrenar."),
]

# NOTE: all data below is clearly-labeled DEMO data (is_demo_data=True), used
# only to populate the catalog UI before an authorized product data source
# (e.g. Amazon Product Advertising API) is connected. Nothing here is scraped
# or presented as real Amazon pricing/availability/review information.
PRODUCTS = {
    "tecnologia": [
        (
            "Audífonos inalámbricos Demo X1",
            "Cancelación de ruido activa, 20h de batería.",
            59.99,
            4.5,
            1280,
            [
                "Cancelación de ruido activa",
                "20 horas de batería",
                "Resistentes al agua IPX4",
            ],
        ),
        (
            "Smartwatch Demo Fit 3",
            "Monitor de salud y notificaciones en la muñeca.",
            89.90,
            4.2,
            643,
            ["Monitor de ritmo cardíaco", "GPS integrado", "Pantalla AMOLED"],
        ),
        (
            "Power bank Demo 20000mAh",
            "Carga rápida para varios dispositivos.",
            34.50,
            4.6,
            2110,
            ["20000mAh de capacidad", "Carga rápida 18W", "3 puertos de salida"],
        ),
        (
            "Cámara web Demo HD Pro",
            "1080p con micrófono integrado para videollamadas.",
            42.00,
            4.1,
            389,
            ["1080p a 30fps", "Micrófono con reducción de ruido", "Clip universal"],
        ),
    ],
    "gaming": [
        (
            "Mouse gamer Demo Strike",
            "Sensor óptico de alta precisión, RGB personalizable.",
            29.99,
            4.4,
            950,
            ["Sensor óptico 16000 DPI", "RGB personalizable", "6 botones programables"],
        ),
        (
            "Teclado mecánico Demo Arc",
            "Switches táctiles, retroiluminado.",
            54.99,
            4.3,
            712,
            [
                "Switches mecánicos táctiles",
                "Retroiluminación RGB",
                "Reposamuñecas incluido",
            ],
        ),
        (
            "Silla gamer Demo Throne",
            "Soporte lumbar ajustable, reclinable 160°.",
            189.00,
            4.0,
            215,
            ["Reclinable hasta 160°", "Soporte lumbar ajustable", "Reposabrazos 4D"],
        ),
        (
            "Audífonos gamer Demo Surround 7.1",
            "Sonido envolvente con micrófono retráctil.",
            44.90,
            4.2,
            530,
            [
                "Sonido envolvente 7.1",
                "Micrófono retráctil",
                "Compatible multiplataforma",
            ],
        ),
    ],
    "hogar": [
        (
            "Aspiradora robot Demo Clean 2",
            "Mapeo inteligente, control por app.",
            199.00,
            4.3,
            1420,
            [
                "Mapeo inteligente láser",
                "Control por app",
                "Hasta 120 min de autonomía",
            ],
        ),
        (
            "Purificador de aire Demo Fresh",
            "Filtro HEPA, ideal para espacios medianos.",
            79.90,
            4.1,
            302,
            [
                "Filtro HEPA H13",
                "Modo nocturno silencioso",
                "Sensor de calidad de aire",
            ],
        ),
        (
            "Set de organizadores Demo Modular",
            "Organizadores apilables para closet.",
            24.99,
            4.5,
            860,
            ["Material resistente", "Apilables y modulares", "Fácil de limpiar"],
        ),
        (
            "Lámpara inteligente Demo Glow",
            "Control por voz y app, 16M de colores.",
            19.99,
            4.0,
            445,
            [
                "16 millones de colores",
                "Compatible con asistentes de voz",
                "Temporizador programable",
            ],
        ),
    ],
    "cocina": [
        (
            "Freidora de aire Demo CrispAir 5L",
            "Cocción sin aceite, 8 programas preestablecidos.",
            69.90,
            4.6,
            1890,
            [
                "Capacidad 5 litros",
                "8 programas preestablecidos",
                "Canasta antiadherente",
            ],
        ),
        (
            "Licuadora Demo Blendmax Pro",
            "Motor de 1200W, jarra de vidrio.",
            49.99,
            4.2,
            670,
            ["Motor de 1200W", "Jarra de vidrio resistente", "6 velocidades"],
        ),
        (
            "Set de cuchillos Demo ChefLine",
            "Acero inoxidable, bloque de madera incluido.",
            39.90,
            4.4,
            520,
            ["Acero inoxidable alemán", "Bloque de madera incluido", "6 piezas"],
        ),
        (
            "Cafetera Demo BrewDaily",
            "Programable, jarra térmica de 1.2L.",
            54.00,
            4.1,
            310,
            ["Programable 24h", "Jarra térmica 1.2L", "Filtro reutilizable"],
        ),
    ],
    "oficina": [
        (
            "Silla ergonómica Demo WorkFit",
            "Soporte lumbar, altura ajustable.",
            159.00,
            4.3,
            480,
            ["Soporte lumbar ajustable", "Reposabrazos ajustables", "Base de 5 ruedas"],
        ),
        (
            'Monitor Demo ViewPro 27"',
            "QHD, 75Hz, ideal para trabajo y multitarea.",
            229.00,
            4.5,
            390,
            ["Resolución QHD 2560x1440", "Panel IPS", "Ajuste de altura e inclinación"],
        ),
        (
            "Escritorio ajustable Demo StandUp",
            "Altura eléctrica ajustable, sentado o de pie.",
            249.00,
            4.2,
            165,
            [
                "Altura eléctrica ajustable",
                "Memoria de 4 posiciones",
                "Superficie de 120x60cm",
            ],
        ),
        (
            "Lámpara de escritorio Demo FocusLight",
            "Luz LED regulable sin parpadeo.",
            27.99,
            4.4,
            540,
            ["LED sin parpadeo", "3 temperaturas de color", "Puerto USB de carga"],
        ),
    ],
    "fitness": [
        (
            "Set de bandas elásticas Demo FlexFit",
            "5 niveles de resistencia, bolsa incluida.",
            18.99,
            4.5,
            1340,
            [
                "5 niveles de resistencia",
                "Material antideslizante",
                "Bolsa de transporte incluida",
            ],
        ),
        (
            "Mancuernas ajustables Demo PowerAdjust",
            "De 2.5 a 24kg en un solo par.",
            149.00,
            4.6,
            410,
            ["Ajustable de 2.5 a 24kg", "Cambio rápido de peso", "Diseño compacto"],
        ),
        (
            "Esterilla de yoga Demo ZenMat",
            "Antideslizante, 6mm de grosor.",
            22.90,
            4.4,
            980,
            [
                "6mm de grosor",
                "Superficie antideslizante",
                "Incluye correa de transporte",
            ],
        ),
        (
            "Botella inteligente Demo HydroTrack",
            "Recordatorios de hidratación, 750ml.",
            24.99,
            4.0,
            275,
            ["Recordatorios de hidratación", "Capacidad 750ml", "Marcadores de nivel"],
        ),
    ],
}


class Command(BaseCommand):
    help = "Carga categorías y productos de demostración (claramente identificados) para probar el catálogo."

    def handle(self, *args, **options):
        created_categories = 0
        for order, (name, slug, description) in enumerate(CATEGORIES):
            _, created = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "description": description, "order": order},
            )
            created_categories += created

        created_products = 0
        asin_seq = 1
        for cat_slug, products in PRODUCTS.items():
            category = Category.objects.get(slug=cat_slug)
            for i, (
                name,
                short_desc,
                price,
                rating,
                review_count,
                features,
            ) in enumerate(products):
                slug = slugify(name)
                asin = f"B0DEMO{asin_seq:04d}"
                asin_seq += 1
                _, created = Product.objects.get_or_create(
                    slug=slug,
                    defaults={
                        "asin": asin,
                        "name": name,
                        "category": category,
                        "short_description": short_desc,
                        "description": f"{short_desc} Producto de demostración para probar el catálogo — no es información real de un listado de Amazon.",
                        "features": "\n".join(features),
                        "price": price,
                        "currency": "USD",
                        "rating": rating,
                        "review_count": review_count,
                        "image_url": f"https://placehold.co/500x500/f4f0ea/333?text={slugify(name)[:20]}",
                        "is_demo_data": True,
                        "is_active": True,
                        "is_featured": i == 0,
                    },
                )
                created_products += created

        self.stdout.write(
            self.style.SUCCESS(
                f"Listo: {created_categories} categorías nuevas, {created_products} productos demo nuevos."
            )
        )
