from django.urls import path
from django.conf.urls import include
from .views import SendOTPphone,validateOTP,Register,LoginAPI,ChangePasswordView,EditProfile
urlpatterns = [
    path('validatePhone',SendOTPphone.as_view() ),
    path('validateOTP', validateOTP.as_view()),
    path('register',Register.as_view()),
    path('login',LoginAPI.as_view()),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('Editprofile', EditProfile.as_view(), name='Edit-profile'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('password_reset/confirm/<str:token>', include('django_rest_passwordreset.urls', namespace='password_reset_confirm')),

]
