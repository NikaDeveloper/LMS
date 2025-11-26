from rest_framework import viewsets
from .models import Course, Lesson
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsModerator, IsOwner
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Просмотр доступен всем авторизованным
            self.permission_classes = [IsAuthenticated]

        elif self.action in ['update', 'partial_update']:  # Редактирование разрешено только модерам или владельцам
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        elif self.action in ['create', 'destroy']:  # Создание и удаление разреш. только авторизованным,
            # которые НЕ являются модераторами
            self.permission_classes = [IsAuthenticated, ~IsModerator]  # ('~' - логическое НЕ)

        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Просмотр
            self.permission_classes = [IsAuthenticated]

        elif self.action in ['update', 'partial_update']:  # Редактирование
            # Разрешено: ИЛИ Модератору, ИЛИ Владельцу
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        elif self.action in ['create', 'destroy']:  # Создание/Удаление
            # Разрешено: НЕ Модератору
            self.permission_classes = [IsAuthenticated, ~IsModerator]

        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
