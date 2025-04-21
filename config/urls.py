"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/auth/', include('apps.auth_app.urls')),  # Rutas de autenticación
    
    path('api/usuarios/', include('apps.usuarios.urls')),  # Rutas de usuarios


    
    path('api/', include('apps.productos.urls')), 
    
    path('api/', include('apps.categoria.urls')), 
    
    path('api/ventas/', include('apps.ventas.urls')), 
    
    path('api/reportes/', include('apps.reportes.urls')), 
    
    path('api/contabilidad/', include('apps.contabilidad.urls')),
    
    path('api/crm/', include('apps.crm.urls')),
    
    path('api/voz/', include('apps.voz.urls')),
    
    path('api/carrito/', include('apps.carrito.urls')),

]
