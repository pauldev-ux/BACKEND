# apps/carrito/urls.py
from django.urls import path
from .views import CarritoView, CalcularTotalView, RealizarPagoView, GenerarReciboView

urlpatterns = [
    path('<int:usuario_id>/'           , CarritoView.as_view(),        name='carrito'),
    path('<int:usuario_id>/total/'     , CalcularTotalView.as_view(),   name='carrito-total'),
    path('<int:usuario_id>/pago/'      , RealizarPagoView.as_view(),    name='carrito-pago'),
    path('<int:usuario_id>/recibo/'    , GenerarReciboView.as_view(),   name='carrito-recibo'),
]
    