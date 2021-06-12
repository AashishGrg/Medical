from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'user_type')

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
