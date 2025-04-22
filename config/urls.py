# config/urls.py

from django.contrib import admin
from django.urls    import path, include
from django.http    import HttpResponse

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticación / Usuarios
    path('api/auth/',     include('apps.auth_app.urls')),
    path('api/usuarios/', include('apps.usuarios.urls')),

    # Catálogo
    path('api/', include('apps.productos.urls')),
    path('api/', include('apps.categoria.urls')),

    # Ventas
    path('api/ventas/', include('apps.ventas.urls')),

    # Resto de apps…
    path('api/reportes/',     include('apps.reportes.urls')),
    path('api/contabilidad/', include('apps.contabilidad.urls')),
    path('api/crm/',          include('apps.crm.urls')),
    path('api/voz/',          include('apps.voz.urls')),

    # Carrito
    path('api/carrito/', include('apps.cart.urls')),

    # Vistas de prueba para Stripe
    path('success/', lambda req: HttpResponse("✅ Pago completado con éxito.")),
    path('cancel/',  lambda req: HttpResponse("❌ Pago cancelado.")),
]
