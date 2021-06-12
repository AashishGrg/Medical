from django.urls import path
from .views import SignupAPIView,LoginAPIView

app_name = 'users'

urlpatterns = [
    path('signup/',SignupAPIView.as_view(),name='signup'),
    path('login/',LoginAPIView.as_view(),name='login'),
]
