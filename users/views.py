from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import User
from .serializers import UserProfileSerializer


class UserProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE для конкретного профиля по ID"""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "pk"
