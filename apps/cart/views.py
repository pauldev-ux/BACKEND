import stripe

from django.conf                    import settings
from django.views.decorators.csrf   import csrf_exempt
from django.utils.decorators        import method_decorator
from django.contrib.auth            import get_user_model

from rest_framework import viewsets, status
from rest_framework.views           import APIView
from rest_framework.response        import Response
from rest_framework.permissions     import IsAuthenticated

from .models      import Cart, CartItem, Payment
from .serializers import CartSerializer, CartItemSerializer
from apps.ventas.services.checkout_service import checkout_usuario

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()


class CartViewSet(viewsets.ModelViewSet):
    """
    /api/carrito/cart/      → GET lista o crea carrito
    /api/carrito/cart/{pk}/ → detalle, update, delete (poco usado)
    """
    serializer_class   = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    /api/carrito/cart-items/      → POST nueva línea
    /api/carrito/cart-items/{pk}/ → PATCH cantidad, DELETE línea
    """
    serializer_class   = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product   = serializer.validated_data['product']
        quantity  = serializer.validated_data['quantity']
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
        self.instance = item

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        data = self.get_serializer(self.instance).data
        return Response(data, status=status.HTTP_201_CREATED)


class CreateCheckoutSessionView(APIView):
    """
    POST /api/carrito/checkout/
    → devuelve { checkout_url } de Stripe para pagar todo el carrito.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items   = cart.items.select_related('product').all()
        if not items:
            return Response(
                {"detail": "El carrito está vacío."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1) Construir los line_items
        line_items = []
        for item in items:
            prod = item.product
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(prod.price * 100),
                    "product_data": {
                        "name":        prod.name,
                        "description": prod.description or "",
                        "images":      [prod.image_url] if prod.image_url else [],
                    },
                },
                "quantity": item.quantity,
            })

        # 2) Crear la Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url= request.build_absolute_uri("/success/") +
                         "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=  request.build_absolute_uri("/cancel/"),
            metadata={"user_id": request.user.id},
        )

        # 3) Devolver sólo la URL de Stripe
        return Response({"checkout_url": session.url})


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):
    """
    POST /api/carrito/webhook/
    → al recibir checkout.session.completed:
        1) registra el Payment,
        2) crea la Venta (checkout_usuario),
        3) vacía el carrito.
    """
    def post(self, request):
        payload    = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event["type"] == "checkout.session.completed":
            sess    = event["data"]["object"]
            user_id = int(sess["metadata"]["user_id"])
            user    = User.objects.get(pk=user_id)

            # 1) Registrar el Payment
            Payment.objects.create(
                usuario           = user,
                payment_intent_id = sess["payment_intent"],
                amount            = sess["amount_total"] / 100,
                currency          = sess["currency"],
                status            = sess["payment_status"],
            )

            # 2) Crear la Venta y vaciar carrito
            try:
                checkout_usuario(user_id)
            except ValueError:
                # carrito vacío o error al crear venta
                pass

        return Response(status=status.HTTP_200_OK)
