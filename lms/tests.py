from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import Group
from users.models import User
from lms.models import Course, Lesson, Subscription

MODERATOR_GROUP_NAME = 'Moderators'


class LMSPermissionsTestCase(APITestCase):
    """ Базовый класс для настройки пользователей и объектов """

    def setUp(self):
        # 1. Настройка пользователей
        self.owner_user = User.objects.create(email="owner@lms.com", phone="1")
        self.owner_user.set_password("owner123")
        self.owner_user.save()

        self.non_owner_user = User.objects.create(email="nonowner@lms.com", phone="2")
        self.non_owner_user.set_password("nonowner123")
        self.non_owner_user.save()

        # Создание группы модераторов и пользователя-модератора
        self.moderator_group, created = Group.objects.get_or_create(name=MODERATOR_GROUP_NAME)
        self.moderator_user = User.objects.create(email="moderator@lms.com", is_staff=True, phone="3")
        self.moderator_user.set_password("moder123")
        self.moderator_user.groups.add(self.moderator_group)
        self.moderator_user.save()

        # 2. Настройка объектов (Владелец - owner_user)
        self.course = Course.objects.create(title="Test Course", owner=self.owner_user)
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            video_url="https://www.youtube.com/watch?v=123",
            owner=self.owner_user
        )

        # 3. URL-адреса
        self.course_list_url = reverse('lms:course-list')
        self.course_detail_url = reverse('lms:course-detail', args=[self.course.pk])
        self.lesson_list_url = reverse('lms:lesson-list')
        self.lesson_detail_url = reverse('lms:lesson-detail', args=[self.lesson.pk])

    # 4. Вспомогательные методы для аутентификации
    def authenticate_as_user(self, user):
        self.client.force_authenticate(user=user)

    def unauthenticate(self):
        self.client.force_authenticate(user=None)


class CourseTestCase(LMSPermissionsTestCase):
    """ Тесты CRUD и прав доступа для модели Course """

    #  READ (LIST/RETRIEVE) Tests (Permission: IsAuthenticated)
    def test_course_list_retrieve_access(self):
        """ Проверка доступа к списку/просмотру (Всем авторизованным 200) """
        self.authenticate_as_user(self.non_owner_user)
        self.assertEqual(self.client.get(self.course_list_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(self.course_detail_url).status_code, status.HTTP_200_OK)

        self.unauthenticate()
        self.assertEqual(self.client.get(self.course_list_url).status_code, status.HTTP_401_UNAUTHORIZED)

    #  CREATE Tests (Permission: IsAuthenticated, ~IsModerator)
    def test_course_create_by_owner(self):
        """ Владелец (не-модератор) может создать курс (201) """
        self.authenticate_as_user(self.owner_user)
        data = {"title": "New Course by Owner"}
        response = self.client.post(self.course_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_create_by_moderator_forbidden(self):
        """ Модератор не может создать курс (403) """
        self.authenticate_as_user(self.moderator_user)
        data = {"title": "Course by Moderator"}
        response = self.client.post(self.course_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #  UPDATE Tests (Permission: IsModerator | IsOwner)
    def test_course_update_by_owner(self):
        """ Владелец может обновить свой курс (200) """
        self.authenticate_as_user(self.owner_user)
        response = self.client.patch(self.course_detail_url, {"title": "Owner Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_update_by_moderator_allowed(self):
        """ Модератор может обновить ЧУЖОЙ курс (200) """
        self.authenticate_as_user(self.moderator_user)
        response = self.client.patch(self.course_detail_url, {"title": "Moderator Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_update_by_non_owner_forbidden(self):
        """ Не владелец не может обновить чужой курс (403) """
        self.authenticate_as_user(self.non_owner_user)
        response = self.client.patch(self.course_detail_url, {"title": "Non-Owner Attempt"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #  DELETE Tests (Permission: IsAuthenticated, IsOwner, ~IsModerator)
    def test_course_delete_by_owner(self):
        """ Владелец может удалить свой курс (204) """
        self.authenticate_as_user(self.owner_user)
        response = self.client.delete(self.course_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_course_delete_by_moderator_forbidden(self):
        """ Модератор НЕ может удалить курс (403) """
        self.authenticate_as_user(self.moderator_user)
        response = self.client.delete(self.course_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_delete_by_non_owner_forbidden(self):
        """ Не владелец не может удалить курс (403) """
        self.authenticate_as_user(self.non_owner_user)
        response = self.client.delete(self.course_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LessonTestCase(LMSPermissionsTestCase):
    """ Тесты CRUD и прав доступа для модели Lesson """

    # CRUD (тестирует, что владелец может)
    def test_lesson_create_retrieve_update_delete_by_owner(self):
        """ Проверка полного CRUD для владельца """
        self.authenticate_as_user(self.owner_user)

        # 1. CREATE
        data = {"title": "New Lesson", "course": self.course.pk, "video_url": "https://www.youtube.com/watch?v=456"}
        response = self.client.post(self.lesson_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_lesson_pk = response.data['id']

        # 2. RETRIEVE
        response = self.client.get(reverse('lms:lesson-detail', args=[new_lesson_pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 3. UPDATE
        response = self.client.patch(reverse('lms:lesson-detail', args=[new_lesson_pk]), {"title": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 4. DELETE
        response = self.client.delete(reverse('lms:lesson-detail', args=[new_lesson_pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #  Permissions Tests
    def test_lesson_update_by_moderator_allowed(self):
        """ Модератор может обновить ЧУЖОЙ урок (200) """
        self.authenticate_as_user(self.moderator_user)
        response = self.client.patch(self.lesson_detail_url, {"title": "Mod Updated Lesson"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create_by_moderator_forbidden(self):
        """ Модератор не может создать урок (403) """
        self.authenticate_as_user(self.moderator_user)
        data = {"title": "Mod Lesson", "course": self.course.pk, "video_url": "https://www.youtube.com/watch?v=789"}
        response = self.client.post(self.lesson_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_by_non_owner_forbidden(self):
        """ Не владелец не может удалить чужой урок (403) """
        self.authenticate_as_user(self.non_owner_user)
        response = self.client.delete(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    """ Тесты для эндпоинта подписки """

    def setUp(self):
        self.user = User.objects.create(email="sub@test.com", password="123")
        self.course = Course.objects.create(title="Sub Course", owner=self.user)
        self.subscribe_url = reverse('lms:course_subscribe')

    def test_subscribe_toggle(self):
        """ Тест подписки и отписки """
        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.pk}

        # Подписываемся
        response = self.client.post(self.subscribe_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Отписываемся
        response = self.client.post(self.subscribe_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscribe_unauthenticated_forbidden(self):
        """ Тест доступа неавторизованного пользователя (401) """
        self.client.force_authenticate(user=None)
        data = {"course_id": self.course.pk}
        response = self.client.post(self.subscribe_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
