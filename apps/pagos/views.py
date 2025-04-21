from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .services import crear_payment_intent

class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Recibe { amount: 123.45 } y devuelve { client_secret }.
        """
        amount = request.data.get("amount")
        if amount is None:
            return Response({"detail": "Se requiere el monto."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            client_secret = crear_payment_intent(request.user, float(amount))
            return Response({"client_secret": client_secret})
        except RuntimeError as e:
            return Response({"detail": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        
        
