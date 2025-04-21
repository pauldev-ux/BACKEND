# apps/usuarios/services/user_service.py
from apps.usuarios.models import User, Role
from django.core.exceptions import ObjectDoesNotExist

def create_user(username, email, password, role_id):
    try:
        role = Role.objects.get(id=role_id)
    except ObjectDoesNotExist:
        raise ValueError(f"El rol con id {role_id} no existe.")
    
    user = User.objects.create_user(username=username, email=email, password=password, role=role)
    return user

def update_user(id, new_data):
    try:
        # Buscar al usuario por su ID
        user = User.objects.get(id=id)

        # Actualizar los campos del usuario
        for key, value in new_data.items():
            setattr(user, key, value)

        # Guardar los cambios
        user.save()
        return user
    except User.DoesNotExist:
        return None


def delete_user(username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        return user
    except User.DoesNotExist:
        return None
