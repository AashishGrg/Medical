from django.urls import path
from .views import SignupAPIView,LoginAPIView,ProfileView,ProfileUpdateAPIView,ProfileDetailUpdateAPIView,PasswordChangeAPIView

app_name = 'users'

urlpatterns = [
    path('signup/',SignupAPIView.as_view(),name='signup'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('profile/detail/',ProfileView.as_view(),name='profile'),
    path('profile/update/',ProfileUpdateAPIView.as_view(),name='profile_update'),
    path('profile/',ProfileDetailUpdateAPIView.as_view(),name='profile_detail_update'),
    path('password/change/',PasswordChangeAPIView.as_view(),name='pwd_change'),
]
