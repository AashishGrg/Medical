from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.api.serializers import SignupSerializer, LoginSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupAPIView(CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)  # getting the data from serializer class
        if serializer.is_valid(raise_exception=True):  # validating the serializer data
            email = serializer.validated_data['email']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            user_type = serializer.validated_data['user_type']
            password = serializer.validated_data['password']
            user = User.objects.create(email=email, first_name=first_name, last_name=last_name, user_type=user_type)
            user.set_password(password)
            user.is_verified = True
            user.save()
            return Response(serializer.data)


class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
            except User.DoesNotExist:
                raise NotFound({"email": "User with the provided email does not exist."})  # exception message
            if not user.check_password(serializer.validated_data['password']):
                raise ValidationError({'password': "Incorrect password"})
            if not (user.is_active or user.is_verified):
                raise ValidationError({'email': "User not activated or is unverfied"})
            token = RefreshToken.for_user(user)  # method to generating access and refresh token for users
            print(dir(token))
            return Response({
                'refresh': str(token),
                'access': str(token.access_token)
            })
