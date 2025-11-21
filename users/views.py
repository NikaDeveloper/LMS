from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import generics
from .models import User, Payment
from .serializers import UserProfileSerializer, PaymentSerializer


class UserProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE для конкретного профиля по ID"""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "pk"


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')

    ordering_fields = ('payment_date', )



