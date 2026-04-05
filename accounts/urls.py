from django.urls import path
from .views import RegisterView, LoginView, PasswordResetRequestView, PasswordResetVerifyView, UserDetailView, ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-verify/', PasswordResetVerifyView.as_view(), name='password-reset-verify'),
    path('profile/', UserDetailView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]