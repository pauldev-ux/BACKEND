from rest_framework import serializers
from apps.usuarios.models import User, Role

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = self.get_default_role()
        user = User.objects.create_user(
            role=role,
            password=password,
            **validated_data
        )
        return user

    def get_default_role(self):
        try:
            return Role.objects.get(name='cliente')
        except Role.DoesNotExist:
            raise serializers.ValidationError("Rol 'cliente' no existe.")
