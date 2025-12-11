from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User, Payment
from lms.models import Course, Lesson  # Нужны для создания Payments


class UserAuthTestCase(APITestCase):
    """Тесты регистрации, логина и общих эндпоинтов User"""

    def setUp(self):
        #  1. Пользователи
        self.owner_user = User.objects.create(
            email="owner@user.com",
            first_name="Owner",
            last_name="Profile",
            phone="12345",
        )
        self.owner_user.set_password("owner123")
        self.owner_user.save()

        self.other_user = User.objects.create(
            email="other@user.com", first_name="Other", last_name="User", phone="54321"
        )
        self.other_user.set_password("other123")
        self.other_user.save()

        #  2. Объекты для связанных данных
        self.course = Course.objects.create(title="Test Course")
        # Создаем платеж для владельца, чтобы проверить вывод в профиле
        Payment.objects.create(user=self.owner_user, course=self.course, amount=1000)

        #  3. URL-адреса
        self.register_url = reverse("users:register")
        self.token_url = reverse("users:token")
        self.owner_profile_url = reverse(
            "users:user-profile", args=[self.owner_user.pk]
        )
        self.other_profile_url = reverse(
            "users:user-profile", args=[self.other_user.pk]
        )

    #  AUTH Tests (AllowAny)
    def test_user_registration(self):
        """Тест успешной регистрации"""
        data = {"email": "new@user.com", "password": "newpassword"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login_success(self):
        """Тест успешного получения токена (логин)"""
        data = {"email": "owner@user.com", "password": "owner123"}
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_user_login_fail(self):
        """Тест ошибки при неверном пароле (401)"""
        data = {"email": "owner@user.com", "password": "wrongpassword"}
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- PROFILE READ Tests (Dynamic Serializer) ---
    def test_profile_retrieve_owner_full_data(self):
        """Владелец видит свой профиль полностью (есть payments, last_name)"""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(self.owner_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что используется UserProfileSerializer
        self.assertIn("payments", response.data)
        self.assertIn("last_name", response.data)
        self.assertTrue(len(response.data["payments"]) > 0)

    def test_profile_retrieve_public_restricted_data(self):
        """Другой пользователь видит профиль урезанно (нет payments, last_name)"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(
            self.owner_profile_url
        )  # other_user смотрит owner_user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что используется UserPublicProfileSerializer
        self.assertNotIn("payments", response.data)
        self.assertNotIn("last_name", response.data)
        self.assertIn("email", response.data)

    # --- PROFILE UPDATE/DELETE Tests (IsOwnerOrReadOnly) ---
    def test_profile_update_by_owner_allowed(self):
        """Владелец может обновить свой профиль (200)"""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.patch(
            self.owner_profile_url, {"first_name": "UpdatedOwner"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_update_by_non_owner_forbidden(self):
        """Другой пользователь не может обновить чужой профиль (403)"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(
            self.owner_profile_url, {"first_name": "Hack Attempt"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PaymentTestCase(APITestCase):
    """Тесты для эндпоинта списка платежей (ListAPIView)"""

    def setUp(self):
        self.user = User.objects.create(email="pay@user.com", password="123")
        self.payments_url = reverse("users:payments-list")
        self.course = Course.objects.create(title="Paid Course")
        # Создаем платеж для фильтрации
        Payment.objects.create(
            user=self.user, course=self.course, amount=500, payment_method="transfer"
        )

    def test_payment_list_unauthenticated_forbidden(self):
        """Список платежей закрыт для неавторизованных (401)"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.payments_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_payment_list_filtering(self):
        """Проверка фильтрации по payment_method"""
        self.client.force_authenticate(user=self.user)

        # Создаем второй платеж
        Payment.objects.create(
            user=self.user, course=self.course, amount=1000, payment_method="cash"
        )

        # Фильтруем по 'transfer'
        response = self.client.get(f"{self.payments_url}?payment_method=transfer")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем длину списка
        self.assertEqual(len(response.data), 1)
