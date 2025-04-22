# apps/ventas/urls.py

from django.urls        import path
from rest_framework.routers import DefaultRouter
from apps.ventas.views  import VentaViewSet, CheckoutView

router = DefaultRouter()
# Registramos el ViewSet en la raíz (''), para list/create en /api/ventas/
router.register(r'', VentaViewSet, basename='ventas')

urlpatterns = [
    # Primero el endpoint de checkout manual
    path('checkout/', CheckoutView.as_view(), name='ventas-checkout'),
    # Luego todas las rutas generadas por el ViewSet:
] + router.urls
