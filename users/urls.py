from django.urls import path
from .views import UserProfileRetrieveUpdateDestroyAPIView

urlpatterns = [
    path(
        "profile/<int:pk>/",
        UserProfileRetrieveUpdateDestroyAPIView.as_view(),
        name="user-profile-detail",
    ),
]
