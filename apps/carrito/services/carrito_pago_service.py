# apps/carrito/services/carrito_pago_service.py
import stripe

# Configuración de Stripe
stripe.api_key = 'tu_api_key'

def realizar_pago(total, tarjeta_info):
    # Implementación de Stripe o alguna pasarela de pago
    try:
        charge = stripe.Charge.create(
            amount=total * 100,  # en centavos
            currency="usd",
            source=tarjeta_info,
            description="Pago de compra",
        )
        return charge
    except stripe.error.CardError as e:
        return str(e)
