from django.urls import path
from .views import UserProfileRetrieveUpdateDestroyAPIView, PaymentListAPIView


app_name = "users"


urlpatterns = [
    path(
        "profile/<int:pk>/",
        UserProfileRetrieveUpdateDestroyAPIView.as_view(),
        name="user-profile-detail",
    ),
    path('payments/', PaymentListAPIView.as_view(), name='payments-list'),
]
