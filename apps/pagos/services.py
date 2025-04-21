import stripe
from django.conf import settings
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def crear_payment_intent(usuario, amount, currency="usd"):
    """
    Crea y confirma un PaymentIntent en Stripe,
    guarda un registro en Payment y devuelve el client_secret.
    """
    try:
        # Stripe trabaja en centavos
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency=currency,
            metadata={"user_id": usuario.id},
            automatic_payment_methods={"enabled": True},
        )
        # Guarda en BD
        Payment.objects.create(
            usuario=usuario,
            payment_intent_id=intent.id,
            amount=amount,
            currency=currency,
            status=intent.status,
        )
        return intent.client_secret
    except stripe.error.StripeError as e:
        raise RuntimeError(f"Stripe error: {e.user_message}")
