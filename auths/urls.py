from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from auths.views import MyObtainTokenPairView

urlpatterns = [
    # path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
