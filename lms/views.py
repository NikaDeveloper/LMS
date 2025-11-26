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

        elif self.action == 'create':
            # Создавать могут все авторизованные, КРОМЕ модераторов
            self.permission_classes = [IsAuthenticated, ~IsModerator]  # ('~' - логическое НЕ)

        elif self.action == 'destroy':
            # Удалять могут ТОЛЬКО владельцы (НЕ модераторы)
            self.permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]

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

        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]  # ('~' - логическое НЕ)

        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]

        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
