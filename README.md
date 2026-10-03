# Zattia

Plataforma de descubrimiento de productos y carrito de compras orientada a marketing de afiliados de Amazon. El sitio **no procesa pagos**: el usuario arma un carrito y es redirigido a Amazon (vía enlace de afiliado) para completar la compra.

## Arquitectura

```
config/            # settings, urls, wsgi/asgi
apps/
  core/            # home, contacto, FAQ, páginas legales
  categories/      # Category, navegación por categoría
  products/        # Product, búsqueda, filtros, detalle, API, demo seed
  cart/            # carrito basado en sesión (services.Cart)
  affiliate/       # construcción de enlaces de afiliado + tracking de clics (/go/<slug>/)
  analytics/       # Event (product_view, search, add_to_cart, amazon_click...) + dashboard
templates/         # base.html + components/ + una carpeta por app
static/            # css/ js/ manifest.json
media/             # imágenes subidas (productos, categorías)
```

Cada app Django vive bajo `apps/` para mantener el namespace limpio; la lógica de negocio que no pertenece a una vista está en `services.py` de cada app (`cart/services.py`, `affiliate/services.py`, `analytics/services.py`, `products/services.py`).

## Instalación

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # y completa los valores
```

### Variables de entorno (`.env`)

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Django. |
| `DEBUG` | `True`/`False`. Nunca `True` en producción. |
| `DATABASE_URL` | `postgres://usuario:password@host:5432/nombre_db` |
| `ALLOWED_HOSTS` | Dominios separados por coma. |
| `AMAZON_AFFILIATE_TAG` | Tu tracking ID de Amazon Associates. |
| `AMAZON_MARKETPLACE` | ej. `amazon.com`, `amazon.com.mx`. |
| `AMAZON_BASE_URL` | Base URL de Amazon (informativo, el link real se arma con el marketplace). |
| `SITE_NAME` | Nombre de marca, usado en todo el sitio. |
| `SITE_URL` | URL pública completa, usada en sitemap/SEO/structured data. |
| `GOOGLE_ANALYTICS_ID` | Opcional. |

### Base de datos (PostgreSQL)

```bash
python manage.py migrate
```

### Crear superusuario

```bash
python manage.py createsuperuser
```

### Cargar datos demo

```bash
python manage.py seed_demo
```

Crea 6 categorías y 24 productos **claramente marcados como demo** (`is_demo_data=True`), con ASINs ficticios (`B0DEMOxxxx`) e imágenes placeholder — no son datos reales de Amazon.

### Ejecutar en desarrollo

```bash
python manage.py runserver
```

### Ejecutar tests

```bash
python manage.py test
```

### Deploy

En producción, detrás de Nginx/un balanceador:

```bash
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2
```

WhiteNoise sirve los estáticos comprimidos incluso sin un proxy al frente (útil en plataformas tipo Render/Railway); en este despliegue Nginx también los sirve directo desde `staticfiles/` por rendimiento.

Con Docker:

```bash
docker compose up --build
```

## Configurar afiliación de Amazon

Toda la lógica de enlaces vive en `apps/affiliate/services.py`:

- `build_amazon_affiliate_url(product)` — enlace de un solo producto.
- `build_amazon_cart_url(cart_items)` — enlace que agrega varios productos al carrito real de Amazon de una vez (Remote Shopping Cart).
- `track_affiliate_click(request, product)` — registra el clic en `AffiliateClick`.

El tag, dominio y base URL se leen de `settings.AMAZON_AFFILIATE_TAG` / `AMAZON_MARKETPLACE` / `AMAZON_BASE_URL` (vía `.env`) — nunca están hardcodeados en templates.

Todo botón "Comprar en Amazon" del sitio enlaza a `/go/<slug-del-producto>/`, no directamente a Amazon — así cada clic queda registrado antes de redirigir.

## API (Django REST Framework)

Pensada para una futura integración (app móvil, etc.), de solo lectura por ahora:

- `GET /api/products/`
- `GET /api/products/<slug>/`
- `GET /api/categories/`
- `GET /api/categories/<id>/`

## Conectar una fuente de datos de Amazon autorizada

`apps/products/services.py` define `AmazonProductService` (interfaz abstracta) y `MockAmazonProductService` (implementación actual, con datos ficticios en código, sin red). Cuando haya acceso a una fuente autorizada (p. ej. la Product Advertising API, una vez la cuenta de Associates califique), se implementa una nueva clase que herede de `AmazonProductService` y se reemplaza el uso de `MockAmazonProductService` — el resto de la app (modelos, vistas, templates) no cambia. **No se hace scraping en ningún punto del proyecto.**

## Seguridad

- CSRF habilitado en todos los formularios y endpoints POST del carrito.
- `SESSION_COOKIE_SECURE` / `CSRF_COOKIE_SECURE` activos cuando `DEBUG=False`.
- `X_FRAME_OPTIONS = DENY` (protección contra clickjacking).
- `SECRET_KEY`, credenciales de base de datos y el tag de afiliado viven solo en variables de entorno, nunca en el repo.
- El carrito solo guarda `{product_id: cantidad}` en la sesión — nunca tarjetas, datos bancarios ni contraseñas de terceros.
