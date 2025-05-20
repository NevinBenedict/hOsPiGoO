from django.urls import path,include
from .views import *
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('regotp/', RegisterVerificationView.as_view(), name='regotp'),
    path('docregister/',DocRegistrationView.as_view(), name='docregister'),
    path('docregotp/', DocRegisterVerificationView.as_view(), name='docregotp'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('forgotpassword/', ForgotPasswordView.as_view(), name='forgotpassword'),
    path('resetpassword/', ResetPasswordView.as_view(), name='resetpassword'),
    path('resetotp/', ForgotPasswordVerificationView.as_view(), name='resetotp'),
    path('resendotp/', ResendOtpView.as_view(), name='resendotp'),
    path('resendregotp/', ResendRegOtpView.as_view(), name='resendregotp'),
    

]