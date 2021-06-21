from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView, ListAPIView, \
    DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, password_validation

from users.api.serializers import SignupSerializer, LoginSerializer, ProfileSerializer, ProfileUpdateSerializer, \
    ProfileDetailSerializer, PasswordChangeSerializer, DoctorSpecialitySerializer, DoctorSpecialityListSerializer
from users.models import DoctorSpeciality

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
            return Response({
                'refresh': str(token),
                'access': str(token.access_token)
            })


class ProfileView(RetrieveAPIView):
    serializer_class = ProfileDetailSerializer
    permission_classes = (IsAuthenticated,)  # this line makes this view login protected

    def get_object(self):  # overriding default behaviour og get_object that is used by retrieve API view
        return self.request.user

    # def retrieve(self, request, *args, **kwargs): # how retrieve api view is processing the data and giving response
    #     obj = self.get_object()
    #     serializer = self.serializer_class(obj)
    #     return Response(serializer.data)


class ProfileUpdateAPIView(UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user  # self.request.user always returns logged in user


class ProfileDetailUpdateAPIView(RetrieveUpdateAPIView):  # using save view for retrieve and update API
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


# Day 4 code
class PasswordChangeAPIView(APIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data,
                                              context={
                                                  'user': request.user
                                              })  # getting data from serializers and passing logged in user data to serializers using context
        if serializer.is_valid(raise_exception=True):  # exception raise if anything goes wrong
            password = serializer.validated_data['new_password']
            user = request.user
            user.set_password(password)  # setting up the new_password for user
            user.save()
            return Response({"success": "Password changed successfully"})


class DoctorSpecialityCreateAPIView(CreateAPIView):
    serializer_class = DoctorSpecialitySerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DoctorSpecialityListAPIView(ListAPIView):
    serializer_class = DoctorSpecialityListSerializer
    permission_class = (IsAuthenticated,)
    queryset = DoctorSpeciality.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = DoctorSpecialityListSerializer(qs, many=True)
        data = serializer.data
        data.append({
            "total": len(qs)
        })
        return Response(data)


class DoctorSpecialityDeleteAPIView(DestroyAPIView):
    serializer_class = DoctorSpecialitySerializer
    permission_classes = (IsAdminUser,)

    def delete(self, request, *args, **kwargs):
        spec = self.kwargs['pk']  # getting id from url
        try:
            doc_spec = DoctorSpeciality.objects.get(id=spec)
            doc_spec.delete()
            return Response({"success": "Selected Speciality deleted successfully."})
        except DoctorSpeciality.DoesNotExist:
            raise NotFound("Speciality does not exist.")


class DoctorSpecialityRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorSpecialitySerializer
    permission_classes = (IsAdminUser,)
    lookup_url_kwarg = 'pk'
    queryset = DoctorSpeciality.objects.all()
