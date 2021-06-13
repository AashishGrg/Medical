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


# Day 3 Codes
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'address',
                  'image',)


class ProfileDetailSerializer(serializers.ModelSerializer):
    get_full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'address',
                  'image', 'is_active', 'is_verified', 'user_type', 'get_full_name')


class ProfileSerializer(serializers.ModelSerializer):
    get_full_name = serializers.ReadOnlyField()  # loading the method of model

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'address',
                  'image', 'is_active', 'is_verified', 'user_type', 'get_full_name')
        read_only_fields = ['email', 'id', 'is_active', 'is_verified',
                            'user_type']  # making fields defined here as uneditable
