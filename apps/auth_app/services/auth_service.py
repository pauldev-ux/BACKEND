from apps.usuarios.models import User

from django.contrib.auth import authenticate

def authenticate_user(username, password):
    return authenticate(username=username, password=password)
