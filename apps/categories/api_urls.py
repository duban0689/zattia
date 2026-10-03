from rest_framework.routers import DefaultRouter

from .api_views import CategoryViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="api-category")

urlpatterns = router.urls
