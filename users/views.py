from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from .permissions import IsOwnerOrReadOnly
from .models import User, Payment
from .serializers import (
    UserProfileSerializer,
    PaymentSerializer,
    UserRegisterSerializer,
    UserPublicProfileSerializer,
)
from .services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
    check_payment_status,
)


class UserCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для регистрации пользователя. Доступен всем, даже неавторизованным"""

    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE для конкретного профиля по ID.
    Доступ закрыт глобальными настройками (нужен токен)"""

    queryset = User.objects.all()

    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        requested_user_id = int(self.kwargs.get("pk"))

        current_user_id = self.request.user.id

        # Если пользователь смотрит свой профиль - полный доступ
        if requested_user_id == current_user_id:
            return UserProfileSerializer

        # Если пользователь смотрит чужой профиль - урезанный доступ
        return UserPublicProfileSerializer


class PaymentListAPIView(generics.ListAPIView):
    """Вывод списка платежей с фильтрацией и сортировкой"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method")

    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(generics.CreateAPIView):
    """эндпоинт для создания платежа"""

    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        # Сохраняем платеж в базе, чтоб получить объект payment
        payment = serializer.save()

        # Определяем за что платим (курс или урок) для названия продукта
        product_name = "Oplata"
        if payment.course:
            product_name = payment.course.title
        elif payment.lesson:
            product_name = payment.lesson.title

        # Создаем продукт в Stripe
        product_id = create_stripe_product(product_name)

        # Создаем цену в Stripe
        price_id = create_stripe_price(product_id, payment.amount)

        # Создаем сессию оплаты и получаем ID сессии и ссылку
        session_id, payment_link = create_stripe_session(price_id)

        # Сохраняем данные в наш объект платежа
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentStatusAPIView(APIView):
    """принимает ID платежа, ищет session_id и спрашивает у Stripe статус"""

    def get(self, request, pk):
        # Получаем платеж по id из базы
        payment = get_object_or_404(Payment, pk=pk)

        # Если есть session_id, проверяем статус в Stripe
        if payment.session_id:
            status_data = check_payment_status(payment.session_id)
            return Response(
                data={"status": status_data, "payment_id": payment.pk},
                status=status.HTTP_200_OK,
            )
        return Response(
            data={"error": "У этого платежа нет Stripe session_id."},
            status=status.HTTP_400_BAD_REQUEST,
        )
