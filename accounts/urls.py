from django.urls import path
from .views import RegisterView, LoginView, PasswordResetRequestView, PasswordResetVerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-verify/', PasswordResetVerifyView.as_view(), name='password-reset-verify'),
]