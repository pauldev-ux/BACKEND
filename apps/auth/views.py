from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.auth.services.auth_service import authenticate_user
from apps.usuarios.serializers import UserSerializer

class LoginView(APIView):
    """
    Autentica a un usuario con username y password.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate_user(username, password)
        if user:
            serializer = UserSerializer(user)
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Credenciales inválidas."},
                            status=status.HTTP_401_UNAUTHORIZED)
