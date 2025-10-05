from django.urls import path

from .accounts import Registerview, WebTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register/', Registerview.as_view(), name='register'),
    path('login/', WebTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]