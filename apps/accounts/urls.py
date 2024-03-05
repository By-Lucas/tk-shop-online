from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView

from accounts.serializers.serializer import MyTokenObtainPairView
from accounts.viewsets.accounts_viewsets import ResetPasswordView, ResetPasswordConfirmView


app_name='accounts'

urlpatterns = [
    path('api/token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/password-reset', ResetPasswordView.as_view(), name='password-reset'),
    path('api/password-reset/confirm', ResetPasswordConfirmView.as_view(), name='password-reset-confirm'),
]
