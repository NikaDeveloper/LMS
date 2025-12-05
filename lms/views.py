from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .paginators import CustomPagination
from .models import Course, Lesson, Subscription
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsModerator, IsOwner
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.views import APIView


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:  # Просмотр доступен всем авторизованным
            self.permission_classes = [IsAuthenticated]

        elif self.action in [
            "update",
            "partial_update",
        ]:  # Редактирование разрешено только модерам или владельцам
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        elif self.action == "create":
            # Создавать могут все авторизованные, КРОМЕ модераторов
            self.permission_classes = [
                IsAuthenticated,
                ~IsModerator,
            ]  # ('~' - логическое НЕ)

        elif self.action == "destroy":
            # Удалять могут ТОЛЬКО владельцы (НЕ модераторы)
            self.permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]

        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        # Получаем id курса из тела запроса
        course_id = request.data.get("course_id")

        # Получаем объект курса, если нет - 404
        course_item = get_object_or_404(Course, id=course_id)

        # Ищем объект подписки
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка есть - удаляем
        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        # Если нет - создаем
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:  # Просмотр
            self.permission_classes = [IsAuthenticated]

        elif self.action in ["update", "partial_update"]:  # Редактирование
            # Разрешено: ИЛИ Модератору, ИЛИ Владельцу
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        elif self.action == "create":
            self.permission_classes = [
                IsAuthenticated,
                ~IsModerator,
            ]  # ('~' - логическое НЕ)

        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]

        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
