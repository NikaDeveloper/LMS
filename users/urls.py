from django.urls import path

from .views import UserProfileRetrieveUpdateDestroyAPIView


app_name = "users"


urlpatterns = [
    path(
        "profile/<int:pk>/",
        UserProfileRetrieveUpdateDestroyAPIView.as_view(),
        name="user-profile-detail",
    ),
]
