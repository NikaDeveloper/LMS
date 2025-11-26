from rest_framework import viewsets
from .models import Course, Lesson
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsModerator
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # просмотр доступен всем авторизованным
            self.permission_classes = [IsAuthenticated]

        elif self.action in ['update', 'partial_update']:  # редактирование разрешено только модерам
            self.permission_classes = [IsAuthenticated, IsModerator]

        elif self.action in ['create', 'destroy']:  # создание и удаление разреш. только авторизованным,
            # которые НЕ являются модераторами
            self.permission_classes = [IsAuthenticated, ~IsModerator]  # ('~' - логическое НЕ)

        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator]

        elif self.action in ['create', 'destroy']:
            # Запрет модератору
            self.permission_classes = [IsAuthenticated, ~IsModerator]

        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]
