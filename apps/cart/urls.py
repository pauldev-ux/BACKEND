from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CartViewSet,
    CartItemViewSet,
    CreateCheckoutSessionView,
    StripeWebhookView,
)

router = DefaultRouter()
router.register(r'cart',       CartViewSet,     basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('',         include(router.urls)),
    path('checkout/', CreateCheckoutSessionView.as_view(), name='checkout'),
    path('webhook/',  StripeWebhookView.as_view(),  name='stripe-webhook'),
]
