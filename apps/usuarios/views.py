# apps/usuarios/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.usuarios.models import User
from apps.usuarios.serializers import UserSerializer
from apps.usuarios.services.user_service import create_user, update_user, delete_user

class UserListView(APIView):
    """
    Muestra todos los usuarios.
    """
    def get(self, request):
        users = User.objects.all()  # Obtener todos los usuarios
        serializer = UserSerializer(users, many=True)  # Serializar los datos
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateView(APIView):
    """
    Crea un nuevo usuario.
    """
  #  permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        role_id = request.data.get("role_id", 1)  # Se espera un ID de rol

        if not username or not email or not password:
            return Response({"detail": "Faltan campos obligatorios."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = create_user(username, email, password, role_id)
            return Response({"detail": "Usuario creado exitosamente."},
                            status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(APIView):
    """
    Actualiza un usuario.
    """
    # permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id): 
        new_data = request.data  # Tomar todos los datos enviados para la actualización

        try:
            # Intentar obtener el usuario por ID
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"detail": "Usuario no encontrado."},
                            status=status.HTTP_404_NOT_FOUND)

        # Actualizar los datos del usuario con los nuevos valores
        for key, value in new_data.items():
            setattr(user, key, value)
        
        user.save()  # Guardar los cambios

        return Response({"detail": f"Usuario {user.username} actualizado."},
                        status=status.HTTP_200_OK)


class UserDeleteView(APIView):
    """
    Elimina un usuario.
    """
  #  permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, username):
        user = delete_user(username)
        if user:
            return Response({"detail": f"Usuario {user.username} eliminado."},
                            status=status.HTTP_200_OK)
        return Response({"detail": "Usuario no encontrado."},
                        status=status.HTTP_404_NOT_FOUND)

class UserDetailView(APIView):
    """
    Muestra los detalles de un usuario específico.
    """
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "Usuario no encontrado."},
                            status=status.HTTP_404_NOT_FOUND)