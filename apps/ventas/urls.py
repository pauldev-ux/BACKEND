# apps/ventas/urls.py
from rest_framework.routers import DefaultRouter
from apps.ventas.views import VentaViewSet

router = DefaultRouter()
router.register(r'ventas', VentaViewSet, basename='ventas')

urlpatterns = router.urls
