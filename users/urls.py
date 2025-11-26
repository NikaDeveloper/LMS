from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserCreateAPIView,
    UserProfileRetrieveUpdateDestroyAPIView,
    PaymentListAPIView,
)


app_name = "users"

urlpatterns = [
    # Регистрация
    path("register/", UserCreateAPIView.as_view(), name="register"),
    # Авторизация (получение токена)
    path("token/", TokenObtainPairView.as_view(), name="token"),
    # Обновление токена
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Профиль и платежи
    path(
        "profile/<int:pk>/",
        UserProfileRetrieveUpdateDestroyAPIView.as_view(),
        name="user-profile",
    ),
    path("payments/", PaymentListAPIView.as_view(), name="payments-list"),
]
