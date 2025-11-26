from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .models import User, Payment
from .serializers import UserProfileSerializer, PaymentSerializer, UserRegisterSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """ Эндпоинт для регистрации пользователя. Доступен всем, даже неавторизованным"""
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """ GET, PUT, PATCH, DELETE для конкретного профиля по ID.
    Доступ закрыт глобальными настройками (нужен токен) """

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "pk"

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class PaymentListAPIView(generics.ListAPIView):
    """ Вывод списка платежей с фильтрацией и сортировкой """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')

    ordering_fields = ('payment_date', )



